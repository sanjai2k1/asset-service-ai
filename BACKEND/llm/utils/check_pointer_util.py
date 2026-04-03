from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
import uuid
from config.settings import settings
from core.logging import logger
from .check_point_registerations import get_registered_serializer
import asyncio

class CheckpointUtil:
    def __init__(self):
        self.pool = AsyncConnectionPool(
            conninfo=settings.postgresql_connection_string,
            max_size=20,
            open=False
        )
        self._checkpointer = AsyncPostgresSaver(self.pool)
        self._checkpointer.serde = get_registered_serializer()

        self._running = True   # ✅ control flag
        self.ready = False     # ✅ health flag

    async def setup(self):
        while self._running:
            try:
                await self.pool.open()
                await self._checkpointer.setup()

                self.ready = True
                return   

            except Exception as e:
                self.ready = False
                logger.error("❌ DB retrying...", exc_info=True)

                await asyncio.sleep(5)   # retry delay
    async def reopen(self):
        try:
            logger.warning("Reopening DB pool...")

            await self.pool.close()

            self.pool = AsyncConnectionPool(
                conninfo=settings.postgresql_connection_string,
                max_size=20,
                open=False
            )

            self._checkpointer = AsyncPostgresSaver(self.pool)
            self._checkpointer.serde = get_registered_serializer()

            await self.pool.open()
            await self._checkpointer.setup()

            self.ready = True

            logger.info("DB pool reopened successfully")
            return {
                "reopen":True
            }

        except Exception:
            self.ready = False
            logger.error(" Failed to reopen DB", exc_info=True)
            return {
                "reopen":False
            }
    async def shutdown(self):
        self._running = False
        try:
            await self.pool.close()
        except Exception:
            pass
    def get_config(self, thread_id: str = None):
        return {
            "configurable": {
                "thread_id": thread_id or str(uuid.uuid4())
            }
        }
    def create_thread_id(self) -> str:
        return str(uuid.uuid4())
    async def is_healthy(self) -> bool:
        try:
            if not self.ready:
                return {
                "status" : True
            }
            async with self.pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT 1;")
                    await cur.fetchone()

            return {
                "status" : True
            }
        except Exception as e:
            return {
                "status" : False,
                "exception" : str(e)
            }


checkpoint_util = CheckpointUtil()
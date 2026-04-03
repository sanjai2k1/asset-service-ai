import asyncio
from sqlalchemy import text
from db.session import engine,engine_ms
from llm.utils.InMemoryMessasageUtil import InMemoryCache
from domain.system.chains import system_chain
from llm.utils.check_pointer_util import checkpoint_util
from db.cache.cache_provider import CacheProvider

class SystemService:

    # --- Health Checks ---
    async def health(self):
        """Check general app health"""
        return {"status": "Application started"}

    async def db_health(self):
        """Check database connectivity separately"""
        try:
            def check():
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
            await asyncio.to_thread(check)
            return {"db": "reachable"}
        except Exception as e:
            return {"db": f"unreachable ({str(e)})"}
    async def sqlserver_db_health(self):
        """Check database connectivity separately"""
        try:
            def check():
                with engine_ms.connect() as conn:
                    conn.execute(text("SELECT 1"))
            await asyncio.to_thread(check)
            return {"db": "reachable"}
        except Exception as e:
            return {"db": f"unreachable ({str(e)})"}
    async def llm_health(self):
        result = system_chain.make_llm_call()

        return result
    async def cache_health(self):
        result = CacheProvider.cache_health()

        return result
    async def checkponter_health(self):
        result = await checkpoint_util.is_healthy()
        return result
    async def checkpointer_reopen(self):
        result = await checkpoint_util.reopen()
        return result
    async def get_all_states(self, thread_id: str):
        config = checkpoint_util.get_config(thread_id)
        states = []

        async for item in checkpoint_util._checkpointer.alist(config):
            states.append(item)


        return     {
        "thread_id": thread_id,
        "count": len(states),
        "data": states
    }
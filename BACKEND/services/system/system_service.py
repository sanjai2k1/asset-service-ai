import asyncio
from sqlalchemy import text
from db.session import engine
from llm.utils.InMemoryMessasageUtil import InMemoryCache
from domain.system.chains import system_chain


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
    async def llm_health(self):
        result = system_chain.make_llm_call()

        return result
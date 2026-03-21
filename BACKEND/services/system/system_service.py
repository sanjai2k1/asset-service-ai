import asyncio
from sqlalchemy import text
from db.session import engine
from llm.graphs.system.system_graph import build_graph
from llm.utils.InMemoryMessasageUtil import InMemoryCache

graph = build_graph()


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
        thread_id = InMemoryCache.create_thread_id()
        result = await graph.ainvoke({},config=InMemoryCache.get_config(thread_id))

        return result
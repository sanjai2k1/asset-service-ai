import asyncio
from sqlalchemy import text
from db.session import engine
from llm.graphs.srcreation.srcreation_graph import build_graph
from schemas.srcreation.classification_result_schema import ClassificationState
from llm.utils.InMemoryMessasageUtil import InMemoryCache
graph = build_graph()


class SrCreationService: 
    # async def sr_create(self,thread_id,request):
    #     if thread_id is None:
    #         thread_id = CheckpointUtil.create_thread_id()
    #     state = ClassificationState(
    #     request=request
    #     )
    #     print(CheckpointUtil.get_config(thread_id))
    #     config = CheckpointUtil.get_config(thread_id)
    #     check_state = await graph.aget_state(config)
    #     print(check_state)
    #     result = await graph.ainvoke(state.model_dump(),config=CheckpointUtil.get_config(thread_id))
    #     print(result)
    #     print("-----service--")
    #     return result
    async def sr_create(self, thread_id, request):
        if thread_id is None:
            thread_id = InMemoryCache.create_thread_id()

        config = InMemoryCache.get_config(thread_id)

        # ❌ NO manual save here
        # ❌ NO assistant save here

        # ✅ Load memory only
        state = InMemoryCache.get_state(thread_id,state_cls=ClassificationState,
    request=request)

        
        result = await graph.ainvoke(
            state,
            config=config
        )

        print(result)
        print("-----service--")

        return result
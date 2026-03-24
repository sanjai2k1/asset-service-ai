import asyncio
from sqlalchemy import text
from db.session import engine
# from llm.graphs.srcreation.srcreation_graph import build_graph
from domain.service_request_creation.graphs.sr_classify_graph import build_graph
from schemas.srcreation.classification_result_schema import ClassificationState
from llm.utils.InMemoryMessasageUtil import InMemoryCache
from llm.utils.check_pointer_util import CheckpointUtil


graph = build_graph()


class SrCreationService: 
 
    async def sr_create(self, thread_id, request):

        if thread_id is None or not thread_id:
            thread_id = CheckpointUtil.create_thread_id()

        config = CheckpointUtil.get_config(thread_id)
        result = await graph.ainvoke({
            "request": request
        },
            config=config)
        if result["is_classification_complete"] and result["is_mandatory_fields_complete"]:
            return {
                "thread_id" : result["thread_id"],
                "aiMessage": {"content": result["final_summary"]},
                "issrcreated" : True}

        return {
            "thread_id" : result["thread_id"],

            "aiMessage": {"content": result["clarification_question"]},
            "issrcreated" : False
            }
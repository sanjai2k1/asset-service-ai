import asyncio
from sqlalchemy import text
from db.session import engine
# from llm.graphs.srcreation.srcreation_graph import build_graph
from domain.service_request_creation.graphs.sr_classify_graph import compile_graph
from schemas.srcreation.classification_result_schema import ClassificationState,GetSRRecordsResponse,GetSRRecordsRequest
from llm.utils.InMemoryMessasageUtil import InMemoryCache
from llm.utils.check_pointer_util import checkpoint_util
from db.services.service_request_service import service_request_service



class SrCreationService: 
 
    async def sr_create(self, thread_id, request):

        if thread_id is None or not thread_id:
            thread_id = checkpoint_util.create_thread_id()
        compiled_graph = compile_graph()
        config = checkpoint_util.get_config(thread_id)
        result = await compiled_graph.ainvoke({
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
    async def sr_create_stream(self, thread_id, request):

        if not thread_id:
            thread_id = checkpoint_util.create_thread_id()

        config = checkpoint_util.get_config(thread_id)

        last_state = None
        compiled_graph = compile_graph()

        async for state in compiled_graph.astream(
            {
                "request": request,
                "current_node": "Identifying User Intent..."
            },
            config=config,
            stream_mode="values"
        ):
            last_state = state

            yield {
                "type": "progress",
                "current_node": state.get("current_node")
            }

            await asyncio.sleep(0)  # ✅ flush each progress

        result = last_state

        # 🔥 IMPORTANT: separate final from last progress
        await asyncio.sleep(1)

        if result["is_classification_complete"] and result["is_mandatory_fields_complete"]:
            yield {
                "type": "final",
                "thread_id": result["thread_id"],
                "aiMessage": {
                    "content": result["final_summary"]
                },
                "issrcreated": True
            }
        else:
            yield {
                "type": "final",
                "thread_id": result["thread_id"],
                "aiMessage": {
                    "content": result["clarification_question"]
                },
                "issrcreated": False
            }
    def get_records(self,request: GetSRRecordsRequest):
        records, total = service_request_service.get_records(
        limit=request.limit,
        offset=request.offset,
        service=request.service,
        request_type=request.request_type
    )
        return GetSRRecordsResponse(
        total_count=total,
        records=[{
            "id": r.id,
            "service": r.service,
            "request_type": r.request_type,
            "data": r.data,
            "final_summary": r.final_summary,
            "created_at": r.created_at,
            "updated_at": r.updated_at
        } for r in records]
    )

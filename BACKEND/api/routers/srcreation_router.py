from fastapi import APIRouter
from core.rest_helper import RestHelper
from services.srcreation.srcreation_service import SrCreationService
from fastapi import Body
from fastapi.responses import StreamingResponse
import json


from  schemas.srcreation.classification_result_schema import ClassificationResult,AskRequest,ClassificationResultAskResponse,GetSRRecordsRequest

from typing import List
router = APIRouter(
    prefix="/srcreation",
    tags=["SR-CREATE"]
)

srcreation_service = SrCreationService()


# @router.post("/ask", response_model=ClassificationResultAskResponse)
@router.post("/ask")
async def ask(data: AskRequest):
    return await RestHelper.execute(srcreation_service.sr_create,data.thread_id,data.request)

@router.post("/ask-stream")
async def ask_stream(data: AskRequest):

    async def event_generator():
        async for chunk in srcreation_service.sr_create_stream(
            data.thread_id,
            data.request
        ):
            # ✅ send raw JSON (NO data:, NO \n\n)
            yield json.dumps(chunk) + "\n"
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


@router.post("/service-requests")
async def get_service_requests(request: GetSRRecordsRequest):
    return await RestHelper.execute(srcreation_service.get_records,request)

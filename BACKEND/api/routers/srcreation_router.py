from fastapi import APIRouter
from core.rest_helper import RestHelper
from services.srcreation.srcreation_service import SrCreationService
from fastapi import Body

from  schemas.srcreation.classification_result_schema import ClassificationResult,AskRequest,ClassificationResultAskResponse

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



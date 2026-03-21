from fastapi import APIRouter
from core.rest_helper import RestHelper
from services.srcreation.srcreation_service import SrCreationService
from fastapi import Body

from  schemas.srcreation.classification_result_schema import ClassificationResult,AskRequestResponse,ClassificationResultAskResponse

from typing import List
router = APIRouter(
    prefix="/srcreation",
    tags=["SR-CREATE"]
)

srcreation_service = SrCreationService()


@router.post("/ask", response_model=ClassificationResultAskResponse)
async def ask( request: str  ,
    thread_id: str | None = None ):
    return await RestHelper.execute(srcreation_service.sr_create,thread_id,request)



from fastapi import APIRouter
from core.rest_helper import RestHelper
from services.system.system_service import SystemService

from schemas.system.system_schema import HealthResponse, DBHealthResponse, PromptVariableResponse ,LLMHealthResponse
from typing import List
router = APIRouter(
    prefix="/system",
    tags=["System"]
)

system_service = SystemService()


@router.get("/health", response_model=HealthResponse)
async def health():
    return await RestHelper.execute(system_service.health)

@router.get("/dbhealth", response_model=DBHealthResponse)
async def db_health():
    return await RestHelper.execute(system_service.db_health)

@router.get("/llmhealth", response_model=LLMHealthResponse)
async def llm_health():
    return await RestHelper.execute(system_service.llm_health)


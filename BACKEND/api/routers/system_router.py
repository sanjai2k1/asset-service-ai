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

@router.get("/postgresdbhealth", response_model=DBHealthResponse)
async def postgres_db_health():
    return await RestHelper.execute(system_service.db_health)

@router.get("/sqlserverdbhealth", response_model=DBHealthResponse)
async def sqlserver_db_health():
    return await RestHelper.execute(system_service.sqlserver_db_health)

@router.get("/llmhealth")
async def llm_health():
    return await RestHelper.execute(system_service.llm_health)

@router.get("/cachehealth")
async def cache_health():
    return await RestHelper.execute(system_service.cache_health)

@router.get("/checkpointerhealth")
async def checkpointer_health():
    return await RestHelper.execute(system_service.checkponter_health)

@router.get("/checkpointerreopen")
async def checkpointer_reopen():
    return await RestHelper.execute(system_service.checkpointer_reopen)


@router.get("/checkpoint/{thread_id}")
async def get_checkpoint_states(thread_id: str):
    return await RestHelper.execute(system_service.get_all_states,thread_id)


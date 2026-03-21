from fastapi import APIRouter
from core.rest_helper import RestHelper
from services.promptvars.promptvars_service import PromptVarsService

from schemas.system.system_schema import HealthResponse, DBHealthResponse, PromptVariableResponse
from typing import List
router = APIRouter(
    prefix="/promptvariables",
    tags=["prompt-variables"]
)

promptvars_service = PromptVarsService()




# --- Prompt Variable Endpoints ---
@router.get("/prompt-variables", response_model=List[PromptVariableResponse])
async def list_all_prompt_variables():
    return await RestHelper.execute(promptvars_service.list_all_prompt_variables)

@router.get("/prompt-variables/{prompt_key}", response_model=List[PromptVariableResponse])
async def list_variables_by_prompt(prompt_key: str):
    return await RestHelper.execute( promptvars_service.list_variables_by_prompt ,prompt_key)

@router.post("/prompt-variables", response_model=PromptVariableResponse)
async def add_prompt_variable(
    prompt_key: str,
    keyword: str,
    description: str | None = None
):
    return await RestHelper.execute(
    promptvars_service.add_prompt_variable,
    prompt_key,
    keyword,
    description
)

@router.delete("/prompt-variables/{var_id}", response_model=PromptVariableResponse)
async def remove_prompt_variable(var_id: int):
    return await RestHelper.execute( promptvars_service.remove_prompt_variable,var_id)
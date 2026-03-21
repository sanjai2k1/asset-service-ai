from fastapi import APIRouter
from core.rest_helper import RestHelper
from services.promptvars.prompt_dependency_service import PromptDependencyService

router = APIRouter(
    prefix="/promptdeps",
    tags=["prompt-dependicies"]
)
prompt_dependency_service = PromptDependencyService()


# --- Create Dependency ---
@router.post("/prompt-dependencies")
async def create_dependency(
    prompt_key_id: int,
    parent_id: int | None = None,
    is_parent: bool = False
):    return await RestHelper.execute(
        prompt_dependency_service.create_dependency,
        prompt_key_id,
        parent_id,
        is_parent
    )


# --- Get Dependency By ID ---
@router.get("/prompt-dependencies/{dependency_id}")
async def get_dependency(dependency_id: int):
    return await RestHelper.execute(
        prompt_dependency_service.get_dependency,
        dependency_id
    )


# --- Get All Dependencies ---
@router.get("/prompt-dependencies")
async def get_all_dependencies():
    return await RestHelper.execute(
        prompt_dependency_service.get_all_dependencies
    )


# --- Get Dependencies By Prompt Key ---
@router.get("/prompt-dependencies/prompt/{prompt_key_id}")
async def get_dependencies_by_prompt(prompt_key_id: int):
    return await RestHelper.execute(
        prompt_dependency_service.get_dependencies_by_prompt,
        prompt_key_id
    )


# --- Update Dependency ---
@router.put("/prompt-dependencies/{dependency_id}")
async def update_dependency(dependency_id: int, parent_id: int | None = None, uasge_description_dep : str |None = None, is_parent: bool | None = None):
    return await RestHelper.execute(
        prompt_dependency_service.update_dependency,
        dependency_id,
        parent_id,
        is_parent,
        uasge_description_dep
    )


# --- Delete Dependency ---
@router.delete("/prompt-dependencies/{dependency_id}")
async def delete_dependency(dependency_id: int):
    return await RestHelper.execute(
        prompt_dependency_service.delete_dependency,
        dependency_id
    )


# --- Get Dependency Tree (Stored Procedure) ---
@router.get("/prompt-dependencies/tree/{start_id}")
async def get_dependency_tree(start_id: int):
    return await RestHelper.execute(
        prompt_dependency_service.get_prompt_dependency_tree,
        start_id
    )
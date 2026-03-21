from db.services.prompt_key_dependency_service import PromptKeyDependencyService
import asyncio

class PromptDependencyService:

    def __init__(self):
        self.prompt_key_dependency = PromptKeyDependencyService()

    # --- Create Dependency ---
    async def create_dependency(self, prompt_key_id: int, parent_id: int | None, is_parent: bool):

        return await asyncio.to_thread(
            self.prompt_key_dependency.create_dependency,
            prompt_key_id,
            parent_id,
            is_parent
        )

    # --- Get Dependency By ID ---
    async def get_dependency(self, dependency_id: int):

        dependency = await asyncio.to_thread(
            self.prompt_key_dependency.get_dependency,
            dependency_id
        )

        if not dependency:
            return {"message": "Dependency not found"}

        return dependency

    # --- Get All Dependencies ---
    async def get_all_dependencies(self):

        return await asyncio.to_thread(
            self.prompt_key_dependency.get_all_dependencies
        )

    # --- Get Dependencies By Prompt Key ---
    async def get_dependencies_by_prompt(self, prompt_key_id: int):

        return await asyncio.to_thread(
            self.prompt_key_dependency.get_dependencies_by_prompt,
            prompt_key_id
        )

    # --- Update Dependency ---
    async def update_dependency(self, dependency_id: int, parent_id=None, is_parent=None,uasge_description_dep = None):

        updated = await asyncio.to_thread(
            self.prompt_key_dependency.update_dependency,
            dependency_id,
            parent_id,
            is_parent,
            uasge_description_dep
        )

        if not updated:
            return {"message": "Dependency not found"}

        return updated

    # --- Delete Dependency ---
    async def delete_dependency(self, dependency_id: int):

        deleted = await asyncio.to_thread(
            self.prompt_key_dependency.delete_dependency,
            dependency_id
        )

        if not deleted:
            return {"message": "Dependency not found"}

        return {"message": "Dependency deleted successfully"}

    # --- Stored Procedure Call ---
    async def get_prompt_dependency_tree(self, start_id: int):

        return await asyncio.to_thread(
            self.prompt_key_dependency.get_prompt_dependency_tree,
            start_id
        )
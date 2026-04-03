import asyncio
from sqlalchemy import text
from db.session import engine
from db.services.prompt_template_variable_service import prompt_template_variable_Service

class PromptVarsService:
    def __init__(self):
        # Initialize services here
        self.prompt_service = prompt_template_variable_Service


    # --- Prompt Template Variables ---
    async def list_all_prompt_variables(self):
        """Return all active prompt template variables"""
        # Call service in a thread because service is sync
        return await asyncio.to_thread(self.prompt_service.list_all_active)

    async def list_variables_by_prompt(self, prompt_key: str):
        """Return active variables for a given prompt"""
        return await asyncio.to_thread(
             self.prompt_service.list_by_prompt_key,prompt_key
        )

    async def add_prompt_variable(self, prompt_key: str, keyword: str, description: str = None):
        """Add a new prompt template variable"""
        return await asyncio.to_thread(
            self.prompt_service.add_variable,
    prompt_key,
    keyword,
    description
        )

    async def remove_prompt_variable(self, var_id: int):
        """Soft delete a prompt template variable"""
        return await asyncio.to_thread(
             self.prompt_service.remove_variable,var_id
        )
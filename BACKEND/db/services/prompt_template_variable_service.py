# app/services/prompt_template_variable_service.py
from db.repository.prompt_template_variable_repository  import PromptTemplateVariableRepository

class PromptTemplateVariableService:
    def __init__(self):
        self.repository = PromptTemplateVariableRepository()

    def list_all_active(self):
        """Return all active variables"""
        return self.repository.get_all_active()

    def list_by_prompt_key(self, prompt_key: str):
        """Return all active variables for a given prompt"""
        return self.repository.get_by_prompt_key(prompt_key)

    def add_variable(self, prompt_key: str, keyword: str, description: str = None):
        """Create a new variable for a prompt template"""
        return self.repository.create(prompt_key, keyword, description)

    def remove_variable(self, var_id: int):
        """Soft delete a variable"""
        return self.repository.soft_delete(var_id)
# app/repositories/prompt_template_variable_repository.py
from db.session import SessionLocal
from db.models.prompt_template_variable import PromptTemplateVariable

class PromptTemplateVariableRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all_active(self):
        return self.db.query(PromptTemplateVariable).filter(
            PromptTemplateVariable.is_deleted == 0
        ).all()

    def get_by_prompt_key(self, prompt_key: str):
        return self.db.query(PromptTemplateVariable).filter(
            PromptTemplateVariable.is_deleted == 0,
            PromptTemplateVariable.prompt_key == prompt_key
        ).all()

    def create(self, prompt_key: str, keyword: str, description: str = None):
        var = PromptTemplateVariable(
            prompt_key=prompt_key,
            keyword=keyword,
            description=description,
        )
        self.db.add(var)
        self.db.commit()
        self.db.refresh(var)
        return var

    def soft_delete(self, var_id: int):
        var = self.db.query(PromptTemplateVariable).filter(
            PromptTemplateVariable.id == var_id
        ).first()
        if var:
            var.is_deleted = 1
            self.db.commit()
        return var
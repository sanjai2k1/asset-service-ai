# app/repositories/prompt_template_variable_repository.py
from db.session import SessionLocal
from db.models.prompt_template_variable import PromptTemplateVariable
from db.session import SessionLocal

class PromptTemplateVariableRepository:

    def get_all_active(self):
        with SessionLocal() as db:
            return db.query(PromptTemplateVariable).filter(
                PromptTemplateVariable.is_deleted == False
            ).all()

    def get_by_prompt_key(self, prompt_key: str):
        with SessionLocal() as db:
            return db.query(PromptTemplateVariable).filter(
                PromptTemplateVariable.is_deleted == False,
                PromptTemplateVariable.prompt_key == prompt_key
            ).all()

    def create(self, prompt_key: str, keyword: str, description: str = None):
        with SessionLocal() as db:
            var = PromptTemplateVariable(
                prompt_key=prompt_key,
                keyword=keyword,
                description=description,
            )
            db.add(var)
            db.commit()
            db.refresh(var)
            return var

    def soft_delete(self, var_id: int):
        with SessionLocal() as db:
            var = db.query(PromptTemplateVariable).filter(
                PromptTemplateVariable.id == var_id
            ).first()

            if var:
                var.is_deleted = True
                db.commit()

            return var
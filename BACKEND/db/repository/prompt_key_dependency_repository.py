from db.session import SessionLocal
from db.models.prompt_key_dependency import PromptKeyDependency
from db.models.prompt_template_variable import PromptTemplateVariable
from datetime import datetime
from sqlalchemy import text


class PromptKeyDependencyRepository:

    def __init__(self):
        self.db = SessionLocal()


    # CREATE
    def create(self, prompt_key_id: int, parent_id: int | None, is_parent: bool):
        record = PromptKeyDependency(
            prompt_key_id=prompt_key_id,
            parent_id=parent_id,
            is_parent=is_parent,
            created_at=datetime.utcnow()
        )

        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        return record


    # GET BY ID
    def get_by_id(self, record_id: int):
        return (
            self.db.query(PromptKeyDependency)
            .filter(PromptKeyDependency.id == record_id)
            .first()
        )

    def get_all_by_parent_id(self, parent_id: int):
        query = (
            self.db.query(PromptKeyDependency, PromptTemplateVariable)
            .join(
                PromptTemplateVariable,
                PromptKeyDependency.prompt_key_id == PromptTemplateVariable.id
            )
            .filter(PromptKeyDependency.parent_id == parent_id)
        )
        
        # Execute and return the list
        return query
    # GET ALL
    def get_all(self):
        return self.db.query(PromptKeyDependency).all()


    # GET BY PROMPT KEY
    def get_by_prompt_key(self, prompt_key_id: int):
        return (
            self.db.query(PromptKeyDependency)
            .filter(PromptKeyDependency.prompt_key_id == prompt_key_id)
            .all()
        )


    # UPDATE
    def update(self, record_id: int, parent_id: int | None = None, is_parent: bool | None = None,uasge_description_dep : str |None = None):

        record = self.get_by_id(record_id)

        if not record:
            return None

        if parent_id is not None:
            record.parent_id = parent_id

        if is_parent is not None:
            record.is_parent = is_parent
        if uasge_description_dep is not None:
            record.uasge_description_dep = uasge_description_dep

        record.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(record)

        return record


    # DELETE
    def delete(self, record_id: int):

        record = self.get_by_id(record_id)

        if not record:
            return False

        self.db.delete(record)
        self.db.commit()

        return True
    def get_prompt_dependency(self, start_id: int):
        query = text("EXEC dbo.sp_get_prompt_dependency :StartId")

        result = self.db.execute(
            query,
            {"StartId": start_id}
        )
        rows = result.mappings().all()

        return rows

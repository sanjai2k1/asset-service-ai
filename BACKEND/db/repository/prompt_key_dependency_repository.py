from db.session import SessionLocal
from db.models.prompt_key_dependency import PromptKeyDependency
from db.models.prompt_template_variable import PromptTemplateVariable
from datetime import datetime
from sqlalchemy import text


class PromptKeyDependencyRepository:

    # ❌ REMOVE __init__ completely (no shared session)

    def create(self, prompt_key_id: int, parent_id: int | None = None, is_parent: bool = False, uasge_description_dep: str | None = None):
        with SessionLocal() as db:
            record = PromptKeyDependency(
                prompt_key_id=prompt_key_id,
                parent_id=parent_id,
                is_parent=is_parent,
                created_at=datetime.utcnow(),
                uasge_description_dep=uasge_description_dep
            )
            db.add(record)
            db.commit()
            db.refresh(record)
            return record

    def get_by_id(self, record_id: int):
        with SessionLocal() as db:
            return db.query(PromptKeyDependency).filter(
                PromptKeyDependency.id == record_id
            ).first()

    def get_all(self):
        with SessionLocal() as db:
            return db.query(PromptKeyDependency).all()

    def get_all_by_parent_id(self, parent_id: int):
        with SessionLocal() as db:
            return (
                db.query(PromptKeyDependency, PromptTemplateVariable)
                .join(
                    PromptTemplateVariable,
                    PromptKeyDependency.prompt_key_id == PromptTemplateVariable.id
                )
                .filter(PromptKeyDependency.parent_id == parent_id)
                .all()
            )

    def get_by_prompt_key(self, prompt_key_id: int):
        with SessionLocal() as db:
            return (
                db.query(PromptKeyDependency)
                .filter(PromptKeyDependency.prompt_key_id == prompt_key_id)
                .all()
            )

    def update(self, record_id: int, parent_id: int | None = None, is_parent: bool | None = None, uasge_description_dep: str | None = None):
        with SessionLocal() as db:
            record = db.query(PromptKeyDependency).filter(
                PromptKeyDependency.id == record_id
            ).first()

            if not record:
                return None

            if parent_id is not None:
                record.parent_id = parent_id
            if is_parent is not None:
                record.is_parent = is_parent
            if uasge_description_dep is not None:
                record.uasge_description_dep = uasge_description_dep

            record.updated_at = datetime.utcnow()

            try:
                db.commit()
                db.refresh(record)
            except:
                db.rollback()
                raise

            return record

    def delete(self, record_id: int):
        with SessionLocal() as db:
            record = db.query(PromptKeyDependency).filter(
                PromptKeyDependency.id == record_id
            ).first()

            if not record:
                return False

            try:
                db.delete(record)
                db.commit()
            except:
                db.rollback()
                raise

            return True

    def get_prompt_dependency(self, start_id: int):
        with SessionLocal() as db:
            try:
                query = text("SELECT * FROM sp_get_prompt_dependency(:start_id)")
                result = db.execute(query, {"start_id": start_id})
                return result.mappings().all()
            except Exception as e:
                db.rollback()
                raise e
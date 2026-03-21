from sqlalchemy import Column, Integer, String, Boolean, DateTime, func,String
from db.base import Base  # Your declarative base

class PromptTemplateVariable(Base):
    __tablename__ = "prompt_template_variables_mst"

    id = Column(Integer, primary_key=True, index=True)
    prompt_key = Column(String(100), nullable=False)
    keyword = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    is_deleted = Column(Boolean, nullable=False, default=False)  # <- Boolean here
    created_at = Column(DateTime, nullable=False, server_default=func.getdate())
    updated_at = Column(DateTime, nullable=True)
    is_user_entry = Column(Boolean, nullable=False, default=False, server_default="0")
    uasge_description = Column(String(100), nullable=False)


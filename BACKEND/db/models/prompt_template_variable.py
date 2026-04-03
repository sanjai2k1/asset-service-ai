from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from db.base import Base  
class PromptTemplateVariable(Base):
    __tablename__ = "prompt_template_variables_mst"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    prompt_key = Column(String(100), nullable=False)
    keyword = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    is_deleted = Column(Boolean, nullable=False, default=False, server_default="FALSE")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)
    is_user_entry = Column(Boolean, nullable=False, default=False, server_default="FALSE")
    uasge_description = Column(Text, nullable=True)
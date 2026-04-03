from sqlalchemy import Column, Integer, Boolean, DateTime, Text, func
from datetime import datetime

from db.base import Base  

class PromptKeyDependency(Base):
    __tablename__ = "prompt_key_dependency"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    prompt_key_id = Column(Integer, nullable=False)
    parent_id = Column(Integer, nullable=True)
    is_parent = Column(Boolean, nullable=False, default=False, server_default="FALSE")
    created_at = Column(DateTime, nullable=True, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)
    uasge_description_dep = Column(Text, nullable=True)
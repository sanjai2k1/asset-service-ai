from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey,String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from db.base import Base  

class PromptKeyDependency(Base):
    __tablename__ = "prompt_key_dependency"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prompt_key_id = Column(Integer, nullable=False)
    parent_id = Column(Integer, nullable=True)
    is_parent = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    uasge_description_dep = Column(String(100), nullable=False)

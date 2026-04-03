from sqlalchemy import Column, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
import uuid
from db.base import Base  




class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    service = Column(Text, nullable=True)
    request_type = Column(Text, nullable=True)

    data = Column(JSONB, nullable=True)

    final_summary = Column(Text, nullable=True)

    document_number = Column(Text, unique=True, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
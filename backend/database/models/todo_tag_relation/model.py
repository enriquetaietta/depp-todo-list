from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from backend.database.database import Base

class TodoTagRelation(Base):
    __tablename__ = "todo_tag_relations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    todo_id = Column(UUID(as_uuid=True), ForeignKey("todos.id"), nullable=False)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime)
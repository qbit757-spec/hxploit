from sqlalchemy import Column, String, Boolean
import uuid
from app.db.base import Base

class Cycle(Base):
    __tablename__ = "cycles"
    
    name = Column(String, unique=True, index=True, nullable=False) # e.g., "2024-I"
    is_current = Column(Boolean, default=True)
    is_closed = Column(Boolean, default=False)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))

from sqlalchemy import Column, String
import uuid
from app.db.base import Base

class Campus(Base):
    __tablename__ = "campuses"
    
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    uuid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))

from sqlalchemy import Column, String
from app.db.base import Base

class Campus(Base):
    __tablename__ = "campuses"
    
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

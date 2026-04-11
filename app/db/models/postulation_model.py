from sqlalchemy import Column, String, ForeignKey, Integer, Enum
import enum
from app.db.base import Base

class PostulationStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"

class Postulation(Base):
    __tablename__ = "postulations"
    
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    student_code = Column(String, index=True, nullable=False)
    career = Column(String, nullable=False)
    
    campus_id = Column(Integer, ForeignKey("campuses.id"), nullable=False)
    status = Column(String, default=PostulationStatus.PENDING)
    
    observations = Column(String, nullable=True) # To store why it's flagged (e.g., "3+ absences in previous cycle")

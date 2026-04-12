from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
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
    cycle_id = Column(Integer, ForeignKey("cycles.id"), nullable=True) # Ligado al ciclo de inscripción
    status = Column(String, default=PostulationStatus.PENDING)
    
    observations = Column(String, nullable=True) # Para inasistencias previas
    
    campus = relationship("Campus")
    cycle = relationship("Cycle")

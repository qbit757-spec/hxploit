from sqlalchemy import Column, Integer, ForeignKey, Boolean, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import date
from app.db.base import Base

class Attendance(Base):
    __tablename__ = "attendances"
    
    date = Column(Date, default=date.today, index=True)
    is_present = Column(Boolean, default=True)
    
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    student = relationship("Student", back_populates="attendances")
    
    cycle_id = Column(Integer, ForeignKey("cycles.id"), nullable=False)
    cycle = relationship("Cycle")
    
    campus_id = Column(Integer, ForeignKey("campuses.id"), nullable=False)
    campus = relationship("Campus")

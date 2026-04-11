from sqlalchemy import Column, Integer, ForeignKey, String
from app.db.base import Base

class AttendanceHistory(Base):
    __tablename__ = "attendance_history"
    
    student_code = Column(String, index=True, nullable=False)
    cycle_name = Column(String, nullable=False)
    total_absences = Column(Integer, default=0)
    total_presences = Column(Integer, default=0)
    
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True) # Optional, code is the primary key for lookup across cycles

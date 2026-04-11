from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.db.base import Base

class Student(Base):
    __tablename__ = "students"
    
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    student_code = Column(String, unique=True, index=True, nullable=False)
    career = Column(String, nullable=False)
    
    campus_id = Column(Integer, ForeignKey("campuses.id"), nullable=False)
    campus = relationship("Campus")
    
    # We might want to link to attendance here
    attendances = relationship("Attendance", back_populates="student")

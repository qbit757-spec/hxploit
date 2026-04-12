from pydantic import BaseModel
from typing import Optional, List
from app.schemas.campus_schema import CampusOut
from app.schemas.attendance_schema import AttendanceOut

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    student_code: str
    career: str
    campus_id: int

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    student_code: Optional[str] = None
    career: Optional[str] = None
    campus_id: Optional[int] = None

class StudentOut(StudentBase):
    id: int
    campus: Optional[CampusOut] = None
    attendances: List[AttendanceOut] = []

    class Config:
        from_attributes = True

from pydantic import BaseModel
from datetime import date
from typing import Optional

class AttendanceBase(BaseModel):
    student_id: int
    cycle_id: int
    campus_id: int
    date: date
    is_present: bool

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    is_present: Optional[bool] = None

class AttendanceOut(AttendanceBase):
    id: int

    class Config:
        from_attributes = True

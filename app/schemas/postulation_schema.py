from pydantic import BaseModel
from typing import Optional
from app.db.models.postulation_model import PostulationStatus

class PostulationBase(BaseModel):
    first_name: str
    last_name: str
    student_code: str
    career: str
    campus_id: int
    cycle_id: Optional[int] = None

class PostulationCreate(PostulationBase):
    pass

class PostulationReview(BaseModel):
    status: PostulationStatus
    observations: Optional[str] = None

class PostulationOut(PostulationBase):
    id: int
    status: PostulationStatus
    observations: Optional[str] = None

    class Config:
        from_attributes = True

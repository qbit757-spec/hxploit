from pydantic import BaseModel
from typing import Optional

class CampusBase(BaseModel):
    name: str
    description: Optional[str] = None

class CampusCreate(CampusBase):
    pass

class CampusUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CampusOut(CampusBase):
    id: int

    class Config:
        from_attributes = True

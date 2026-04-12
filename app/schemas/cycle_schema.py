from pydantic import BaseModel
from typing import Optional

class CycleBase(BaseModel):
    name: str
    is_current: bool = True
    is_closed: bool = False

class CycleCreate(CycleBase):
    pass

class CycleOut(CycleBase):
    id: int
    uuid: str

    class Config:
        from_attributes = True

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import deps
from app.schemas.campus_schema import CampusCreate, CampusOut
from app.db.models.campus_model import Campus

router = APIRouter()

@router.get("/", response_model=List[CampusOut])
async def read_campuses(
    db: AsyncSession = Depends(deps.get_db)
):
    stmt = select(Campus)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=CampusOut)
async def create_campus(
    campus_in: CampusCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    db_obj = Campus(**campus_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import deps
from app.schemas.cycle_schema import CycleCreate, CycleOut
from app.db.models.cycle_model import Cycle
from app.services.cycle_service import cycle_service

router = APIRouter()

@router.get("/", response_model=List[CycleOut])
async def read_cycles(
    db: AsyncSession = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    stmt = select(Cycle)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=CycleOut)
async def create_cycle(
    cycle_in: CycleCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user = Depends(deps.check_admin_role)
):
    db_obj = Cycle(**cycle_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.post("/{cycle_id}/close", response_model=CycleOut)
async def close_cycle(
    cycle_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user = Depends(deps.check_admin_role)
):
    cycle = await cycle_service.close_current_cycle(db, cycle_id)
    if not cycle:
        raise HTTPException(status_code=404, detail="Cycle not found or already closed")
    return cycle

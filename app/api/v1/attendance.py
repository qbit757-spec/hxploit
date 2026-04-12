from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.api import deps
from app.schemas.attendance_schema import AttendanceCreate, AttendanceOut
from app.db.models.attendance_model import Attendance
from app.db.models.cycle_model import Cycle
from app.db.models.attendance_history_model import AttendanceHistory

router = APIRouter()

@router.post("/", response_model=AttendanceOut)
async def create_attendance(
    *,
    db: AsyncSession = Depends(deps.get_db),
    attendance_in: AttendanceCreate,
    current_user = Depends(deps.get_current_active_user)
):
    # Check if a record already exists for this student/date/cycle
    stmt = select(Attendance).where(
        Attendance.student_id == attendance_in.student_id,
        Attendance.date == attendance_in.date,
        Attendance.cycle_id == attendance_in.cycle_id
    )
    existing = (await db.execute(stmt)).scalars().first()
    if existing:
        existing.is_present = attendance_in.is_present
        db.add(existing)
    else:
        existing = Attendance(**attendance_in.model_dump())
        db.add(existing)
    
    await db.commit()
    await db.refresh(existing)
    return existing

@router.get("/history/{student_code}", response_model=List[dict])
async def get_student_history(
    student_code: str,
    db: AsyncSession = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    stmt = select(AttendanceHistory).where(AttendanceHistory.student_code == student_code)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/report", response_model=List[AttendanceOut])
async def get_attendance_report(
    db: AsyncSession = Depends(deps.get_db),
    campus_id: int = Query(None),
    cycle_id: int = Query(None),
    current_user = Depends(deps.get_current_active_user)
):
    stmt = select(Attendance).options(
        selectinload(Attendance.student),
        selectinload(Attendance.cycle),
        selectinload(Attendance.campus)
    )
    if campus_id:
        stmt = stmt.where(Attendance.campus_id == campus_id)
    if cycle_id:
        stmt = stmt.where(Attendance.cycle_id == cycle_id)
    
    result = await db.execute(stmt)
    return result.scalars().all()

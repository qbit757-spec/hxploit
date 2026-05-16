from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.api import deps
from app.schemas.student_schema import StudentCreate, StudentOut, StudentUpdate
from app.db.models.student_model import Student
from app.db.models.attendance_model import Attendance

router = APIRouter()

@router.post("/", response_model=StudentOut)
async def create_student(
    *,
    db: AsyncSession = Depends(deps.get_db),
    student_in: StudentCreate,
    current_user = Depends(deps.get_current_active_user)
):
    # Check if student code unique
    result = await db.execute(select(Student).where(Student.student_code == student_in.student_code))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Student code already exists")
    
    db_obj = Student(**student_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    # Refresh with relationships
    stmt = select(Student).where(Student.id == db_obj.id).options(
        selectinload(Student.campus),
        selectinload(Student.attendances)
    )
    result = await db.execute(stmt)
    return result.scalars().first()

@router.get("/", response_model=List[StudentOut])
async def read_students(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    campus_id: int = Query(None),
    current_user = Depends(deps.get_current_active_user)
):
    stmt = select(Student).options(
        selectinload(Student.campus),
        selectinload(Student.attendances)
    ).offset(skip).limit(limit)
    if campus_id:
        stmt = stmt.where(Student.campus_id == campus_id)
    
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/{student_id}", response_model=StudentOut)
async def read_student(
    student_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    stmt = select(Student).where(Student.id == student_id).options(
        selectinload(Student.campus),
        selectinload(Student.attendances)
    )
    result = await db.execute(stmt)
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

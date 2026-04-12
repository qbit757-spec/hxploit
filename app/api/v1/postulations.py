from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.api import deps
from app.schemas.postulation_schema import PostulationCreate, PostulationOut, PostulationReview
from app.db.models.postulation_model import Postulation, PostulationStatus
from app.services.postulation_service import postulation_service
from app.db.models.student_model import Student

router = APIRouter()

# PUBLIC ENDPOINT
@router.post("/public/register", response_model=PostulationOut)
async def public_register(
    *,
    db: AsyncSession = Depends(deps.get_db),
    postulation_in: PostulationCreate
):
    postulation = await postulation_service.create_postulation(db, postulation_in.model_dump())
    # Load relationship for response
    stmt = select(Postulation).where(Postulation.id == postulation.id).options(selectinload(Postulation.campus))
    result = await db.execute(stmt)
    return result.scalars().first()

# ADMIN ENDPOINTS
@router.get("/", response_model=List[PostulationOut])
async def read_postulations(
    db: AsyncSession = Depends(deps.get_db),
    status: PostulationStatus = Query(None),
    campus_id: int = Query(None),
    current_user = Depends(deps.get_current_active_user)
):
    stmt = select(Postulation)
    if status:
        stmt = stmt.where(Postulation.status == status)
    if campus_id:
        stmt = stmt.where(Postulation.campus_id == campus_id)
        
    result = await db.execute(stmt)
    return result.scalars().all()

@router.patch("/{postulation_id}/review", response_model=PostulationOut)
async def review_postulation(
    postulation_id: int,
    review: PostulationReview,
    db: AsyncSession = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    postulation = await db.get(Postulation, postulation_id)
    if not postulation:
        raise HTTPException(status_code=404, detail="Postulation not found")
    
    postulation.status = review.status
    postulation.observations = review.observations
    
    if review.status == PostulationStatus.APPROVED:
        # Convert postulation to student
        new_student = Student(
            first_name=postulation.first_name,
            last_name=postulation.last_name,
            student_code=postulation.student_code,
            career=postulation.career,
            campus_id=postulation.campus_id
        )
        db.add(new_student)
    
    await db.commit()
    await db.refresh(postulation)
    return postulation

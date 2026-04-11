from fastapi import APIRouter
from app.api.v1 import auth, students, attendance, cycles, postulations

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(cycles.router, prefix="/cycles", tags=["cycles"])
api_router.include_router(postulations.router, prefix="/postulations", tags=["postulations"])

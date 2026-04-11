from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.postulation_model import Postulation, PostulationStatus
from app.db.models.student_model import Student
from app.db.models.attendance_history_model import AttendanceHistory
from app.db.models.cycle_model import Cycle

class PostulationService:
    @staticmethod
    async def create_postulation(db: AsyncSession, postulation_in: dict):
        student_code = postulation_in["student_code"]
        
        # Check if student code already exists in active students
        stmt_student = select(Student).where(Student.student_code == student_code)
        student_exists = (await db.execute(stmt_student)).scalars().first()
        
        # Check history for 3+ absences in the last cycle
        stmt_history = (
            select(AttendanceHistory)
            .where(AttendanceHistory.student_code == student_code)
            .order_by(AttendanceHistory.created_at.desc())
        )
        last_history = (await db.execute(stmt_history)).scalars().first()
        
        observations = []
        if student_exists:
            observations.append("ALUMNO_YA_REGISTRADO")
        
        if last_history and last_history.total_absences >= 3:
            observations.append(f"BLOQUEO_POR_INASISTENCIA: {last_history.total_absences} faltas en ciclo {last_history.cycle_name}")
        
        postulation = Postulation(
            **postulation_in,
            observations=" | ".join(observations) if observations else None
        )
        
        db.add(postulation)
        await db.commit()
        await db.refresh(postulation)
        return postulation

postulation_service = PostulationService()

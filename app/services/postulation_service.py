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
        
        # Resolve UUIDs if present
        campus_uuid = postulation_in.pop("campus_uuid", None)
        cycle_uuid = postulation_in.pop("cycle_uuid", None)
        
        if campus_uuid:
            from app.db.models.campus_model import Campus
            stmt_campus = select(Campus.id).where(Campus.uuid == campus_uuid)
            campus_id = (await db.execute(stmt_campus)).scalars().first()
            if campus_id:
                postulation_in["campus_id"] = campus_id
        
        if cycle_uuid:
            stmt_cycle_uuid = select(Cycle.id).where(Cycle.uuid == cycle_uuid)
            cycle_id = (await db.execute(stmt_cycle_uuid)).scalars().first()
            if cycle_id:
                postulation_in["cycle_id"] = cycle_id

        # 1. Obtener ciclo actual si no viene especificado
        if not postulation_in.get("cycle_id"):
            stmt_cycle = select(Cycle).where(Cycle.is_current == True)
            current_cycle = (await db.execute(stmt_cycle)).scalars().first()
            if current_cycle:
                postulation_in["cycle_id"] = current_cycle.id
        
        # 2. Check if student code already exists in active students
        stmt_student = select(Student).where(Student.student_code == student_code)
        student_exists = (await db.execute(stmt_student)).scalars().first()
        
        # 3. Check history for 3+ absences in any past cycle
        stmt_history = (
            select(AttendanceHistory)
            .where(
                AttendanceHistory.student_code == student_code,
                AttendanceHistory.total_absent >= 3
            )
            .order_by(AttendanceHistory.created_at.desc())
        )
        bad_history = (await db.execute(stmt_history)).scalars().first()
        
        observations = []
        if student_exists:
            observations.append("ALUMNO_YA_REGISTRADO")
        
        if bad_history:
            observations.append(f"BLOQUEO_POR_INASISTENCIA: tuvo {bad_history.total_absent} faltas en el ciclo {bad_history.cycle_name}")
        
        postulation = Postulation(
            **postulation_in,
            observations=" | ".join(observations) if observations else None
        )
        
        db.add(postulation)
        await db.commit()
        await db.refresh(postulation)
        return postulation

postulation_service = PostulationService()

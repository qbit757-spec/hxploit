from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.cycle_model import Cycle
from app.db.models.attendance_model import Attendance
from app.db.models.attendance_history_model import AttendanceHistory
from app.db.models.student_model import Student

class CycleService:
    @staticmethod
    async def close_current_cycle(db: AsyncSession, cycle_id: int):
        # 1. Get the cycle
        cycle = await db.get(Cycle, cycle_id)
        if not cycle or cycle.is_closed:
            return None
        
        # 2. Get attendance summaries for this cycle
        stmt = (
            select(
                Student.id,
                Student.student_code,
                func.count().filter(Attendance.is_present == True).label("presences"),
                func.count().filter(Attendance.is_present == False).label("absences")
            )
            .join(Attendance, Attendance.student_id == Student.id)
            .where(Attendance.cycle_id == cycle_id)
            .group_by(Student.id)
        )
        
        results = await db.execute(stmt)
        
        # 3. Save to History
        for row in results:
            history = AttendanceHistory(
                student_id=row.id,
                student_code=row.student_code,
                cycle_name=cycle.name,
                total_present=row.presences,
                total_absent=row.absences
            )
            db.add(history)
        
        # 4. Mark cycle as closed
        cycle.is_closed = True
        cycle.is_current = False
        
        await db.commit()
        return cycle

cycle_service = CycleService()

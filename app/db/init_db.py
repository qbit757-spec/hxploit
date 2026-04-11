import asyncio
import structlog
from tenacity import retry, stop_after_attempt, wait_fixed
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import engine, SessionLocal
from app.db.base import Base
# Import all models here for SQLAlchemy to recognize them
from app.db.models.user_model import User, UserRole
from app.db.models.campus_model import Campus
from app.db.models.student_model import Student
from app.db.models.cycle_model import Cycle
from app.db.models.attendance_model import Attendance
from app.db.models.postulation_model import Postulation
from app.db.models.attendance_history_model import AttendanceHistory
from app.core.security import get_password_hash
from sqlalchemy import select

logger = structlog.get_logger()

@retry(
    stop=stop_after_attempt(10),
    wait=wait_fixed(2),
    before_sleep=lambda retry_state: logger.info("Esperando a la base de datos...", attempt=retry_state.attempt_number)
)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        # Create default campuses
        campus_names = ["San Miguel", "San Isidro", "Monterrico", "Villa"]
        for name in campus_names:
            result = await session.execute(select(Campus).where(Campus.name == name))
            if not result.scalars().first():
                session.add(Campus(name=name))
        
        # Create default admin user if not exists
        result = await session.execute(select(User).where(User.username == "admin"))
        if not result.scalars().first():
            hashed_password = get_password_hash("admin123")
            session.add(User(
                username="admin", 
                hashed_password=hashed_password, 
                role=UserRole.ADMIN
            ))
            
        # Create a default cycle if none exists
        result = await session.execute(select(Cycle).where(Cycle.is_current == True))
        if not result.scalars().first():
            session.add(Cycle(name="2024-I", is_current=True))

        await session.commit()

if __name__ == "__main__":
    asyncio.run(init_db())

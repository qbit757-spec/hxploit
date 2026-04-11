from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user_model import User
from app.repositories.base_repo import BaseRepo

class UserRepo(BaseRepo[User]):
    async def get_by_username(self, db: AsyncSession, username: str) -> User:
        stmt = select(User).where(User.username == username)
        result = await db.execute(stmt)
        return result.scalars().first()

user_repo = UserRepo(User)

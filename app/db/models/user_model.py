from sqlalchemy import Column, String, Enum
import enum
from app.db.base import Base

class UserRole(str, enum.Enum):
    PROFESOR = "profesor"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default=UserRole.PROFESOR)

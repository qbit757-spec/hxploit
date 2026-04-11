from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.api import deps
from app.core import security
from app.core.config import settings
from app.schemas.auth_schema import Token, LoginRequest
from app.schemas.user_schema import UserCreate, UserOut
from app.repositories.user_repo import user_repo

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserCreate
):
    user = await user_repo.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    
    # Create user
    user_data = user_in.model_dump(exclude={"password"})
    user_data["hashed_password"] = security.get_password_hash(user_in.password)
    return await user_repo.create(db, obj_in=user_data)

@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(deps.get_db),
    # Swagger UI usage
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = await user_repo.get_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refresh_token": security.create_refresh_token(user.id),
        "token_type": "bearer",
    }

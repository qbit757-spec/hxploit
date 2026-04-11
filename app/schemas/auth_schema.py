from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    refresh: Optional[bool] = False

class LoginRequest(BaseModel):
    username: str
    password: str

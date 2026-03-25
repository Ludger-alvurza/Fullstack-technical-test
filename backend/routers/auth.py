"""
Router: Authentication
POST /login → JWT access token
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from core.security import authenticate_user, create_access_token

router = APIRouter(tags=["Authentication"])


class LoginRequest(BaseModel):
    username: str
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [{"username": "admin", "password": "admin123"}]
        }
    }


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    full_name: str


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login dan dapatkan JWT token",
    description=(
        "Gunakan credential dummy: **admin / admin123** atau **user / user123**.\n\n"
        "Token dikembalikan sebagai Bearer token untuk endpoint yang dilindungi."
    ),
)
def login(body: LoginRequest) -> LoginResponse:
    user = authenticate_user(body.username, body.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(data={"sub": user["username"]})
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        username=user["username"],
        full_name=user["full_name"],
    )

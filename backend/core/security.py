"""
Security utilities: JWT creation & verification, OAuth2 dependency.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, DUMMY_USERS, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# ── Token Creation ─────────────────────────────────────────────────────────────

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Buat JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ── Token Verification ────────────────────────────────────────────────────────

def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependency: verifikasi JWT token dari Authorization header.
    Raise 401 jika token tidak valid atau expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token tidak valid atau telah kadaluarsa",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username not in DUMMY_USERS:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception


# ── User Authentication ───────────────────────────────────────────────────────

def authenticate_user(username: str, password: str) -> Optional[dict]:
    """Validasi username + password dari DUMMY_USERS."""
    user = DUMMY_USERS.get(username)
    if not user or user["password"] != password:
        return None
    return user

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
   return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
   return pwd_context.verify(plain, hashed)


# --- simple jwt helpers (you can extend as needed) ---


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt
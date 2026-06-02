from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from app.core.settings import settings

password_hasher = PasswordHash(
    hashers=[
        Argon2Hasher(
            time_cost=3,
            memory_cost=65536,
            parallelism=4,
        )
    ],
)


def hash_password(password: str) -> str:
    """Hash the password using configured Argon2 parameters."""
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify the password against the stored hash."""
    return password_hasher.verify(password, hashed_password)


def create_access_token(user_id: str) -> str:
    """Create a JWT access token for an authenticated user."""
    payload = {
        "sub": user_id,
        "type": "access",
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Decode and validate the access token."""
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

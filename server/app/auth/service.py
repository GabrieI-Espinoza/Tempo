from fastapi import HTTPException, status

from app.auth.schemas import RegisterRequest, LoginRequest
from app.core.security import verify_password, hash_password, create_access_token
from app.tortoise.models.user import User


async def register_new_user(data: RegisterRequest) -> dict:
    """Register a new user and return an access token."""
    if await User.filter(email=data.email).exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    user = await User.create(
        email=data.email,
        password_hash=hash_password(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
    )

    token = create_access_token(str(user.user_id))
    return {"access_token": token, "token_type": "bearer", "user": user}


async def authenticate_user(data: LoginRequest) -> dict:
    """Validate user credentials and generate an access token."""
    user = await User.get_or_none(email=data.email)
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    token = create_access_token(str(user.user_id))
    return {"access_token": token, "token_type": "bearer", "user": user}

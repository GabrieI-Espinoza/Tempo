from fastapi import HTTPException, status
from app.tortoise.models.user import User
from app.core.security import verify_password, hash_password, create_access_token
from app.auth.schemas import RegisterRequest, LoginRequest


# Function to register a new user
async def register_new_user(data: RegisterRequest):
    # Check if the email is already registered
    if await User.filter(email=data.email).exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    # Create the new user
    user = await User.create(
        email=data.email,
        password_hash=hash_password(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
    )

    # Generate JWT access token
    token = create_access_token(str(user.user_id))
    # Return the access token and user info
    return {"access_token": token, "token_type": "bearer", "user": user}


# Function to authenticate a user and generate an access token
async def authenticate_user(data: LoginRequest):
    # Retrieve user by email
    user = await User.get_or_none(email=data.email)
    # Verify user existence and password
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    # Generate JWT access token
    token = create_access_token(str(user.user_id))
    # Return the access token and user info
    return {"access_token": token, "token_type": "bearer", "user": user}

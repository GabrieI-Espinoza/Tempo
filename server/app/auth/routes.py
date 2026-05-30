from fastapi import APIRouter, Depends, Request, status

from app.core.limiter import limiter
from app.auth.dependencies import get_current_user
from app.auth.schemas import RegisterRequest, LoginRequest, LoginResponse, UserResponse
from app.auth.service import register_new_user, authenticate_user
from app.tortoise.models.user import User

# APIRouter for authentication routes
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
async def register(request: Request, data: RegisterRequest):
    return await register_new_user(data)


@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")
async def login(request: Request, data: LoginRequest):
    return await authenticate_user(data)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

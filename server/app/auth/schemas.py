from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


# Schema for user registration request
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str
    last_name: str


# Schema for user login request
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Schema for user response
class UserResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    first_name: str
    last_name: str


# Schema for user login response
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

    class Config:
        # Allows this response schema to be created directly from an User model instance
        from_attributes = True

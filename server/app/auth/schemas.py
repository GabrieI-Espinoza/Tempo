import re
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# Schema for user registration request
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str
    last_name: str

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")
        return value


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

    # Allows this response schema to be created directly from an User model instance
    model_config = ConfigDict(from_attributes=True)

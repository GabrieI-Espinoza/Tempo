from pydantic import BaseModel
from app.categories.categories import CategoryLabel, ColorCode


# Schema for category response
class CategoryResponse(BaseModel):
    key: str
    label: CategoryLabel
    color_code: ColorCode

    class Config:
        from_attributes = True  # Enable ORM mode for Tortoise ORM models

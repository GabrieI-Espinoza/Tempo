from pydantic import BaseModel
from app.categories.categories import CategoryLabel, ColorCode


# Schema for category response
class CategoryResponse(BaseModel):
    key: str
    label: CategoryLabel
    color_code: ColorCode

    class Config:
        # Allows this response schema to be created directly from a Category model instance
        from_attributes = True

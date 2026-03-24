from pydantic import BaseModel, ConfigDict
from app.categories.categories import CategoryLabel, ColorCode


# Schema for category response
class CategoryResponse(BaseModel):
    key: str
    label: CategoryLabel
    color_code: ColorCode

    # Allows this response schema to be created directly from a Category model instance
    model_config = ConfigDict(from_attributes=True)

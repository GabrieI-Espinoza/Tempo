from typing import List
from fastapi import APIRouter

from app.categories.schemas import CategoryResponse
from app.categories.service import get_categories

# APIRouter for category routes
router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryResponse])
async def list_all_categories():
    return get_categories()

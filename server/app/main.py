from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.tortoise.config import TORTOISE_ORM
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import settings

from app.auth.routes import router as auth_router
from app.categories.routes import router as categories_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(categories_router)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,  # Set to True only in development
    add_exception_handlers=True,
)

# Make note of CORS settings for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}

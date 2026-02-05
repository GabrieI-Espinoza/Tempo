from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.tortoise.config import TORTOISE_ORM
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import settings

from app.auth.routes import router as auth_router
from app.categories.routes import router as categories_router
from app.event.routes import router as event_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(event_router)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,  # Set to True only in development
    add_exception_handlers=True,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Test endpoint to verify the server is running
@app.get("/")
async def root():
    return {"message": "Hello, Tempo is running!"}

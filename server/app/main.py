from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from tortoise.contrib.fastapi import RegisterTortoise

from app.core.limiter import limiter
from app.core.settings import settings
from app.tortoise.config import TORTOISE_ORM
from app.auth.routes import router as auth_router
from app.categories.routes import router as categories_router
from app.event.routes import router as event_router
from app.note.routes import router as note_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with RegisterTortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=settings.GENERATE_SCHEMAS,
        add_exception_handlers=True,
    ):
        yield


def add_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def add_routes(app: FastAPI) -> None:
    app.include_router(auth_router)
    app.include_router(categories_router)
    app.include_router(event_router)
    app.include_router(note_router)


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]
    add_middleware(app)
    add_routes(app)

    # Test endpoint to verify the server is running
    @app.get("/")
    async def root():
        return {"message": f"Hello, {settings.PROJECT_NAME} is running!"}

    return app


app = create_app()

from app.core.settings import settings

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.tortoise.models.user",
                "app.tortoise.models.event",
                "app.tortoise.models.note",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}

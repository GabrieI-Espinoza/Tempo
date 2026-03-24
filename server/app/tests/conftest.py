import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from asgi_lifespan import LifespanManager

from app.main import app
from app.tortoise.models.note import Note
from app.tortoise.models.event import Event
from app.tortoise.models.user import User


@pytest_asyncio.fixture
async def client():
    # In charge of starting the app and providing a test client, runs once per test every test
    async with LifespanManager(app):
        # Set up virtual server, so testing can begin
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver",
        ) as ac:
            # Provide the client to the test functions
            yield ac


# Will run before each test
@pytest_asyncio.fixture(autouse=True)
async def clear_db(client):
    # Clear the database before each test
    await Note.all().delete()
    await Event.all().delete()
    await User.all().delete()
    yield

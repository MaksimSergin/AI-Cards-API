import pytest
import asyncio
from app import create_app
from app.models.base import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config.config import get_db
from httpx import AsyncClient

app = create_app()

@pytest.fixture(scope="function")
def event_loop():
    """Create a fresh event loop for each test."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def async_engine():
    """Create a database engine for each test."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="function")
async def async_session_maker(async_engine):
    """Create a session maker for each test."""
    TestingSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
    yield TestingSessionLocal

@pytest.fixture(scope="function")
async def override_get_db(async_session_maker):
    """Override the get_db dependency with a fresh session."""
    async def _override_get_db():
        async with async_session_maker() as session:
            yield session
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def client(override_get_db):
    """Create an HTTP client for each test."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

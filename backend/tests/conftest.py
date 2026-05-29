import os

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.database import Base, get_db
from backend.main import app

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://admin:admin@localhost:5433/test_microblog",
)

engine_test = create_async_engine(TEST_DATABASE_URL)

TestingSessionLocal = async_sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac

async def create_user(client, name):
    response = await client.post(
        "/api/users",
        json={"name": name},
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert "api_key" in data

    return data
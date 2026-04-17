import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

import app.models  # noqa: F401 — 注册 ORM 元数据
from app.db.database import Base, engine
from app.main import app

pytestmark = pytest.mark.integration

TRUNCATE_SQL = text(
    "TRUNCATE order_discounts, room_orders, user_auths, rooms, shops, merchants, users "
    "RESTART IDENTITY CASCADE"
)


@pytest_asyncio.fixture(scope="session")
async def _db_ready():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as exc:
        pytest.skip(f"PostgreSQL 不可用（请启动数据库并创建 moonite_test 或设置 TEST_DATABASE_URL）: {exc}")


@pytest_asyncio.fixture(scope="session")
async def ensure_schema(_db_ready):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture(autouse=True)
async def clean_db(ensure_schema):
    async with engine.begin() as conn:
        await conn.execute(TRUNCATE_SQL)
    yield


@pytest_asyncio.fixture
async def client(clean_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

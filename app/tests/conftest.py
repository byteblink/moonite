"""在任何测试导入 app 之前设置数据库连接（优先于 .env）。"""
import os

os.environ.setdefault(
    "DATABASE_URL",
    os.getenv("TEST_DATABASE_URL", "postgresql+asyncpg://postgres:test@127.0.0.1:5432/moonite_test"),
)

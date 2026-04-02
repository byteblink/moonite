### 本地开发环境

复制环境变量模板后按需修改：

```bash
cp .env.example .env
```

本地启动

```bash
uv venv
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Docker Compose（API + Postgres）**

```bash
docker compose up --build -d
```

- API：`http://127.0.0.1:${HOST_PORT:-8000}`（默认 8000）
- 在 Compose 内启动的 `api` 服务默认 `DATABASE_URL` 已指向主机名 `db`；若在宿主机单独跑 `uvicorn`，`.env` 中请使用 `127.0.0.1` 连接映射出来的数据库端口。

**仅启动 Postgres（与旧说明等价，数据卷为命名卷 `moonite_pg_data`）**

```bash
docker compose up -d db
```

### 数据库迁移与管理 (Alembic)

本项目使用 [Alembic](https://alembic.sqlalchemy.org/) 进行数据库版本控制和变更管理。在配置好 `.env` 中的 `DATABASE_URL` 并且本地数据库就绪后，可以通过以下命令管理表结构：

**1. 初始化/更新全部数据表**
当你全新启动本地数据库，或拉取了带新表结构的最新代码后，执行此命令自动建表和更新：
```bash
alembic upgrade head
```
*(注：项目早期的 `resource/sql/` 初始化脚本已被废弃并作为历史归档，请以此方式为准。)*

**2. 基于模型变更生成迁移脚本**
如果你修改了 `app/models/` 下的数据模型类，你需要生成一份变更脚本：
```bash
alembic revision --autogenerate -m "这里填写修改的简短描述，如 add_xxx_field"
```

**3. 审查与应用**
生成脚本后，建议先人工预览一下 `alembic/versions/` 目录里新生成的 Python 代码。确认无误后，再次将更改应用到数据库：
```bash
alembic upgrade head
```


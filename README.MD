### 本地开发环境

复制环境变量模板后按需修改：

```bash
cp .env.example .env
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

数据库初始化脚本见 `resource/sql/`（按文件名依赖顺序执行）。

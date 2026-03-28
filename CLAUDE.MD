# 共享智能空间项目

## 项目简介

这是一个共享智能空间项目，旨在通过共享智能空间，实现资源共享，提高资源利用效率，降低资源浪费，提高生活质量。

## 数据库设计
  见resource/sql目录下的sql文件

## Tech Stack
  python 3.13.12
  fastapi 0.135.2
  sqlalchemy 2.0.48
  alembic 1.18.4
  pytest + httpx: testing
  jwt: auth
  redis: cache
  Celery + Redis: task queue
  postgres: database
  postgis: spatial database
  loguru: logging
  
## 项目结构
  .
  app
  ├── main.py              # FastAPI 启动入口
  ├── api/  
  │   ├── v1/
  │   │   ├── endpoints.py
  │   │   └── routes.py
  │   └── __init__.py
  ├── core/                 
  │   ├── database.py
  │   ├── config.py
  │   ├── logger.py
  │   └── __init__.py
  ├── models/               # ORM 模型
  ├── db/                   # 数据库初始化和连接
  ├── crud/                 # 数据库操作封装
  ├── services/             # 业务逻辑封装
  ├── schemas/              # Pydantic 数据验证
  ├── utils/                # 工具函数
  ├── tasks/                # 异步任务（Celery）
  ├── tests/                # 测试
  ├── docs/                 # 文档
  ├── requirements.txt      # 依赖


## API 设计

### 通用响应格式
其中code为状态码，message为状态信息，data为数据，timestamp为时间戳，request_id为请求ID。
```
{
  "code": 0, // 状态码 0: 成功, 其它: 失败
  "message": "success",
  "data": {}, // 数据 
  "timestamp": 1743120000000, // 时间戳
  "request_id": "1234567890", // 请求ID
}
```

### 两端API设计
  - 用户端API设计以/app开头; 管理后台API设计以/admin开头
 
###
  先实现管理后台的API, 先不考虑auth, 提供基础的CRUD操作。
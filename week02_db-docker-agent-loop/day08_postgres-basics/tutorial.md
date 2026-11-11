# Day 08 · PostgreSQL 基础

> 11/18（周一） · 建议时长 1.5h · 第 2 周

## 今日目标
用 Docker 启动 PostgreSQL，并让代码能存取对话记录。

## 衔接
- 前一天：Function Calling（下）+ 周复盘
- 后一天：Docker 基础

## 学习内容
- 关系型数据库基本概念
- 建表、CRUD、索引
- Python 连接：psycopg 或 SQLAlchemy

## 学习资料（按顺序学习）

| 学习点 | 资料 | 读哪部分 | 预计 |
|---|---|---|---|
| PostgreSQL 入门 | [PostgreSQL 官方教程](https://www.postgresql.org/docs/current/tutorial.html) | 读第 2 章 SQL 语言 | 40 min |
| Docker 启动 Postgres | [Docker Hub：postgres 镜像](https://hub.docker.com/_/postgres) | 看环境变量与 docker run 示例 | 10 min |
| Python 连接 | [psycopg 3：Basic usage](https://www.psycopg.org/psycopg3/docs/basic/usage.html) | 读 Connection、Cursor | 20 min |
| ORM（二选一） | [SQLAlchemy 2.0 Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html) | 只读 Engine、Core 插入与查询 | 30 min |

> 更多概念与延伸阅读见 [reference.md](reference.md)。先读资料再动手，卡住时回到对应小节。

## 练习步骤
1. 安装 Docker，`docker run` 启动 postgres 并映射端口
2. 设计 `messages(id, session_id, role, content, created_at)`
3. 在 `session_id` 上建索引
4. 用代码写入并读取一段对话

## 今日产出
- [ ] `messages` 表与建表 SQL
- [ ] 存取脚本

## 自测
- 不看资料，能否口述今天的核心流程？
- 遇到卡点超过 30 分钟：先保留产出，砍掉拓展内容，不顺延。

## 备注
提示：先用同步方式跑通，后续再换 asyncpg 或异步 SQLAlchemy。

参考资料见同目录 [reference.md](reference.md)。

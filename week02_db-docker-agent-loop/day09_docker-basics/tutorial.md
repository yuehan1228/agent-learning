# Day 09 · Docker 基础

> 11/19（周二） · 建议时长 1.5h · 第 2 周

## 今日目标
把 FastAPI 服务容器化。

## 衔接
- 前一天：PostgreSQL 基础
- 后一天：docker-compose + Redis

## 学习内容
- 镜像、容器、Dockerfile 层缓存
- volume、端口映射、环境变量
- `.dockerignore`

## 学习资料（按顺序学习）

| 学习点 | 资料 | 读哪部分 | 预计 |
|---|---|---|---|
| Docker 概念 | [Docker：Get started](https://docs.docker.com/get-started/) | 读 Docker concepts 与第一个容器部分 | 30 min |
| Dockerfile 写法 | [Docker：Build best practices](https://docs.docker.com/build/building/best-practices/) | 读 Multi-stage、层缓存相关部分 | 20 min |
| uv 与 Docker | [uv：Using uv in Docker](https://docs.astral.sh/uv/guides/integration/docker/) | 读 Installing a project 示例 | 15 min |

> 更多概念与延伸阅读见 [reference.md](reference.md)。先读资料再动手，卡住时回到对应小节。

## 练习步骤
1. 编写 Dockerfile（python:3.11-slim，先复制依赖文件再复制代码）
2. `docker build` 并 `docker run -p 8000:8000 --env-file .env`
3. 在容器内访问 `/docs` 验证

## 今日产出
- [ ] `Dockerfile` 与 `.dockerignore`
- [ ] 可运行的容器

## 自测
- 不看资料，能否口述今天的核心流程？
- 遇到卡点超过 30 分钟：先保留产出，砍掉拓展内容，不顺延。

## 备注
常见坑：容器内 localhost 指容器自身，访问其它容器需用服务名。

参考资料见同目录 [reference.md](reference.md)。

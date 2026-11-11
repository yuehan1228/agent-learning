# Day 10 · docker-compose + Redis

> 11/20（周三） · 建议时长 1.5h · 第 2 周

## 今日目标
用 compose 一键启动 API、Postgres、Redis，并用 Redis 缓存会话。

## 衔接
- 前一天：Docker 基础
- 后一天：对话持久化

## 学习内容
- compose 服务编排、网络、depends_on、healthcheck
- Redis 基本数据结构与 TTL

## 学习资料（按顺序学习）

| 学习点 | 资料 | 读哪部分 | 预计 |
|---|---|---|---|
| compose 入门 | [Docker：Compose Quickstart](https://docs.docker.com/compose/gettingstarted/) | 跟着做一遍 | 25 min |
| 启动顺序 | [Docker：Control startup order](https://docs.docker.com/compose/how-tos/startup-order/) | 读 healthcheck + depends_on condition | 10 min |
| Redis 入门 | [Redis：Get started](https://redis.io/docs/latest/develop/get-started/) | 读 Data structures 部分 | 20 min |
| Python 客户端 | [redis-py 文档](https://redis-py.readthedocs.io/en/stable/) | 读 Connecting、基本命令示例 | 15 min |

> 更多概念与延伸阅读见 [reference.md](reference.md)。先读资料再动手，卡住时回到对应小节。

## 练习步骤
1. 编写 `docker-compose.yml`（api、postgres、redis）
2. API 通过服务名连接数据库和 Redis
3. 用 Redis list 或 string 缓存最近对话，并设置 TTL
4. `docker compose up` 验证

## 今日产出
- [ ] `docker-compose.yml`
- [ ] Redis 缓存读写示例

## 自测
- 不看资料，能否口述今天的核心流程？
- 遇到卡点超过 30 分钟：先保留产出，砍掉拓展内容，不顺延。

## 备注
提示：Postgres 数据请挂载 volume，否则 down 后数据丢失。

参考资料见同目录 [reference.md](reference.md)。

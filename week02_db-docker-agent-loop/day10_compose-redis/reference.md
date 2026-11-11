# Day 10 · docker-compose + Redis · 参考资料

## 关键概念
- **服务发现**：同一 compose 网络内使用服务名互访。
- **healthcheck**：保证数据库就绪后再启动 API。
- **TTL**：缓存过期策略，避免内存无限增长。

## 参考与延伸阅读
- Docker Compose 文档
- Redis 官方入门
- redis-py 文档

## 补充说明
提示：Postgres 数据请挂载 volume，否则 down 后数据丢失。

返回教学文档：[tutorial.md](tutorial.md)

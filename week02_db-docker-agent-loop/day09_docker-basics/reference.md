# Day 09 · Docker 基础 · 参考资料

## 关键概念
- **层缓存**：依赖文件放在代码之前复制，可加速重复构建。
- **env-file**：通过运行时注入密钥，不要写进镜像。
- **0.0.0.0**：容器内服务需监听 0.0.0.0 才能被外部访问。

## 参考与延伸阅读
- Docker 官方 Get Started
- Dockerfile 最佳实践
- uv 的 Docker 集成指南

## 补充说明
常见坑：容器内 localhost 指容器自身，访问其它容器需用服务名。

返回教学文档：[tutorial.md](tutorial.md)

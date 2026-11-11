# Day 04 · FastAPI 入门 · 参考资料

## 关键概念
- **ASGI**：FastAPI 基于的异步服务接口规范，uvicorn 为其服务器。
- **response_model**：约束并过滤返回字段。
- **Depends**：声明并复用依赖，如 LLM 客户端单例。

## 参考与延伸阅读
- FastAPI 官方教程 https://fastapi.tiangolo.com/tutorial/
- Uvicorn 文档
- Starlette 文档

## 补充说明
提示：把 AsyncOpenAI 客户端放到启动阶段创建，不要每次请求新建。

返回教学文档：[tutorial.md](tutorial.md)

# Day 03 · asyncio 进阶 + Pydantic · 参考资料

## 关键概念
- **Semaphore**：限制同时进行的协程数，避免触发 API 限流（429）。
- **结构化输出**：通过 prompt、JSON mode 或 schema 约束输出格式。
- **校验-重试**：把 ValidationError 文本反馈给模型，是 Agent 自我修正的最小形态。

## 参考与延伸阅读
- Pydantic v2 文档 https://docs.pydantic.dev
- httpx 文档 https://www.python-httpx.org
- OpenAI Structured Outputs 指南

## 补充说明
注意：模型常在 JSON 外包裹 ```json 围栏，解析前需清理。

返回教学文档：[tutorial.md](tutorial.md)

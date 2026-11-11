# Day 05 · 流式输出 · 参考资料

## 关键概念
- **SSE**：基于 HTTP 的单向服务端推送，浏览器可用 EventSource 消费。
- **首 token 延迟 TTFT**：流式的核心收益：用户更早看到输出。
- **异步生成器**：`async def` 加 `yield`，是流式响应的基础。

## 参考与延伸阅读
- MDN: Server-sent events
- OpenAI Streaming 文档
- sse-starlette 项目

## 补充说明
排错：如果输出被缓冲、一次性返回，检查代理（如 nginx）是否关闭了缓冲。

返回教学文档：[tutorial.md](tutorial.md)

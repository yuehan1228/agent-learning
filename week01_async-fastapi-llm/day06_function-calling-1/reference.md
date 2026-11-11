# Day 06 · Function Calling（上） · 参考资料

## 关键概念
- **tool_call_id**：回传结果时必须对应，否则 API 报错。
- **description**：工具描述的质量直接决定模型是否选对工具。
- **并行工具调用**：一次响应含多个 tool_calls，可用 asyncio.gather 并发执行。

## 参考与延伸阅读
- OpenAI Function Calling 指南
- DeepSeek Function Calling 文档
- Anthropic Tool use 文档

## 补充说明
思考：模型只“提议”调用，真正执行在你的代码里，这是安全边界的所在。

返回教学文档：[tutorial.md](tutorial.md)

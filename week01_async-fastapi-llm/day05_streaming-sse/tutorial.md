# Day 05 · 流式输出

> 11/15（周五） · 建议时长 1.5h · 第 1 周

## 今日目标
实现逐 token 返回的流式接口，理解 SSE 协议。

## 衔接
- 前一天：FastAPI 入门
- 后一天：Function Calling（上）

## 学习内容
- LLM 的 `stream=True` 与 chunk 结构
- SSE 格式：`data: ...\n\n`
- FastAPI `StreamingResponse`

## 学习资料（按顺序学习）

| 学习点 | 资料 | 读哪部分 | 预计 |
|---|---|---|---|
| SSE 协议 | [MDN：使用服务器发送事件（中文）](https://developer.mozilla.org/zh-CN/docs/Web/API/Server-sent_events/Using_server-sent_events) | 读事件流格式部分 | 15 min |
| 流式响应 | [FastAPI：Custom Response（StreamingResponse）](https://fastapi.tiangolo.com/advanced/custom-response/) | 找到 StreamingResponse 小节 | 15 min |
| LLM 流式输出 | [OpenAI：Streaming responses](https://platform.openai.com/docs/guides/streaming-responses) | 看 chunk 结构与示例 | 15 min |

> 更多概念与延伸阅读见 [reference.md](reference.md)。先读资料再动手，卡住时回到对应小节。

## 练习步骤
1. 先在脚本中迭代打印流式 chunk
2. 实现 `POST /chat/stream`，媒体类型 `text/event-stream`
3. 用 `curl -N` 验证，并处理结束标记 `[DONE]`

## 今日产出
- [ ] 流式接口
- [ ] `curl -N` 的验证输出

## 自测
- 不看资料，能否口述今天的核心流程？
- 遇到卡点超过 30 分钟：先保留产出，砍掉拓展内容，不顺延。

## 备注
排错：如果输出被缓冲、一次性返回，检查代理（如 nginx）是否关闭了缓冲。

参考资料见同目录 [reference.md](reference.md)。

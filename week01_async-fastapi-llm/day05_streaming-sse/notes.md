# Day 05 笔记：流式输出（SSE）

## 运行方式
```bash
cd week01_async-fastapi-llm/day05_streaming-sse
python -m uvicorn stream_response:app --reload
curl -N -X POST localhost:8000/chat/stream -H 'Content-Type: application/json' -d '{"message":"用三句话介绍 FastAPI"}'
```

## curl -N 验证输出
```
data: {"type": "delta", "content": "1. **FastAPI 是一个基于现代 Python 类型提示的高性能 Web 框..."}
data: {"type": "delta", "content": "运行速度可媲美 NodeJS 和 Go。**\n2. **它原生支持异步并发..."}
data: {"type": "delta", "content": "并深度整合 Pydantic，能自动进行严格的数据验证与类型..."}
data: {"type": "delta", "content": " **同时，它开箱即用即可自动生成交互式 API 文档（如 Sw..."}
data: {"type": "delta", "content": "、测试以及前后端协作的效率。**"}
data: {"type": "usage", "usage": 676}
data: [DONE]
```
（内容为节选，每条事件后有一个空行。）

错误场景（API key 错误）：
```
data: {"type": "error", "message": "LLM 调用失败: AuthenticationError"}
data: [DONE]
```
空消息 → HTTP 422，不进入流式。

## 事件约定
| type | 含义 |
|---|---|
| `delta` | 增量文本 `content` |
| `usage` | 本次总 token 数 |
| `error` | 出错信息（只含异常类型） |
| `[DONE]` | 结束标记，**正常或出错都会发送** |

## 要点
1. **SSE 格式**：`data: <内容>\n\n`，两个换行是一条事件的分隔；`media_type="text/event-stream"`。
2. **流式接口的错误无法改 HTTP 状态码**：响应头在第一个字节发出时已经是 200，所以错误只能用 `error` 事件告知，客户端需同时处理 HTTP 错误和流内错误。
3. **不要把 `str(e)` 返回给调用方**：上游原始错误会泄露内部信息；详细内容写日志（`logger.exception`），调用方只看到异常类型。
4. **客户端断开要停止上游**：循环中检查 `request.is_disconnected()`，断开时 `stream.close()`，否则上游继续生成并消耗 token 和并发名额。已用真实 HTTP 连接验证，断开后 `close()` 被调用。
5. **结束标记大小写**：约定为 `[DONE]`，之前写成 `[Done]`，按约定匹配的客户端会认不出。

## 现象：所有 delta 几乎同时到达
- curl 带时间戳观察：全部 delta 在约 10ms 内到达。
- 直接测上游：首个事件约 4.8s 后才出现，之后事件几乎一起出来。
- 原因：该模型是推理型，思考完才集中输出，首 token 延迟（TTFT）高；**不是接口代码的问题**。接口本身是逐事件转发的，换用非推理模型会更明显。

## 取舍
- `Semaphore` 包住整个流式过程：并发超过 5 时，后到的请求在连接建立前无反馈（会一直等待）。当前规模可接受。
- 断开检测只在收到上游事件时才触发；上游长时间无事件时，不会立即发现断开。

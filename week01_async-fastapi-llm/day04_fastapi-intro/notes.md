# Day 04 笔记：FastAPI 入门

## 运行方式
```bash
cd week01_async-fastapi-llm/day04_fastapi-intro
python -m uvicorn app.main:app --reload
# 浏览器打开 http://127.0.0.1:8000/docs 即 Swagger 页面
```
需要 `.env`：`API_BASE_URL`、`OPENAI_API_KEY`、`MODEL_NAME`。

## 接口
| 方法 | 路径 | 请求体 | 响应 |
|---|---|---|---|
| GET | `/health` | 无 | `{"status":"ok"}` |
| POST | `/chat` | `{"message": "..."}`（必填、非空） | `{"reply": "..."}` |

## 调用记录（命令行验证，`/docs` 页面同样可以交互调用）
```
$ GET /health
{"status":"ok"}

$ POST /chat {"message":"用一句话介绍 FastAPI"}
{"reply":"**FastAPI 是一个基于现代 Python 类型提示的高性能 Web 框架，旨在以极快的编码速度构建 API，并原生支持自动生成交互式接口文档。**"}

$ POST /chat {"message":""}            -> 422  String should have at least 1 character
$ POST /chat {}                        -> 422  Field required (body.message)
$ GET /docs                            -> 200
$ 并发 2 个 /chat 期间 GET /health      -> 0.002 s（事件循环未被阻塞）
$ 使用错误 API key 调用 /chat           -> 502 {"detail":"LLM 调用失败: AuthenticationError"}
```

## 要点
1. **客户端放进 lifespan**：启动时创建一次 `AsyncOpenAI`，通过 `Depends(get_llm)` 注入，关闭时 `close()`，避免每次请求新建连接。
2. **必须用异步客户端 + await**：用同步 `OpenAI` 放进 `async def`，会在等待模型时卡住整个服务（实测并发时 `/health` 从 0.002s 变成 6.76s）。
3. **请求/响应模型**：`ChatRequest` 做入参校验（空串、缺字段自动 422），`response_model=ChatResponse` 约束出参。
4. **错误处理**：上游模型报错（`APIError`）转成 502，和自身 bug 导致的 500 区分开。

## 待办与取舍
- 目前没有保存对话历史，每次请求都是独立的单轮（Day 11 解决）。
- 502 的 detail 只返回异常类型，不暴露上游完整错误；排查时需要查看服务日志。

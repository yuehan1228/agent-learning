# Day 03 · asyncio 进阶 + Pydantic

> 11/13（周三） · 建议时长 1.5h · 第 1 周

## 今日目标
掌握并发控制，并让 LLM 输出可被程序可靠消费的结构化数据。

## 衔接
- 前一天：asyncio 基础
- 后一天：FastAPI 入门

## 学习内容
- `Semaphore` 限流、`asyncio.wait_for` 超时
- `httpx.AsyncClient` 的使用
- Pydantic v2：BaseModel、Field、校验、`model_validate_json`

## 学习资料（按顺序学习）

| 学习点 | 资料 | 读哪部分 | 预计 |
|---|---|---|---|
| Semaphore 限流 | [Python 官方：Synchronization Primitives](https://docs.python.org/3/library/asyncio-sync.html) | 只读 Semaphore 小节 | 10 min |
| 超时 wait_for | [Python 官方：Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html) | 读 Timeouts 与 wait_for | 10 min |
| httpx 异步 | [httpx：Async Support](https://www.python-httpx.org/async/) | 通读 | 15 min |
| Pydantic 模型 | [Pydantic：Models](https://docs.pydantic.dev/latest/concepts/models/) | 读 Basic model usage、Validation | 25 min |
| JSON 解析校验 | [Pydantic：JSON](https://docs.pydantic.dev/latest/concepts/json/) | 读 JSON Parsing（model_validate_json） | 10 min |
| 结构化输出概念 | [OpenAI：Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) | 了解 JSON mode 与 schema 的区别 | 15 min |

> 更多概念与延伸阅读见 [reference.md](reference.md)。先读资料再动手，卡住时回到对应小节。

## 练习步骤
1. 对 20 个请求用 Semaphore(5) 限流并设置超时
2. 让 LLM 按指定 schema 输出 JSON
3. 用 Pydantic 校验，失败时把错误信息回传模型并重试（最多 3 次）

## 今日产出
- [ ] `structured_output.py`
- [ ] 一份失败重试的日志样例

## 自测
- 不看资料，能否口述今天的核心流程？
- 遇到卡点超过 30 分钟：先保留产出，砍掉拓展内容，不顺延。

## 备注
注意：模型常在 JSON 外包裹 ```json 围栏，解析前需清理。

参考资料见同目录 [reference.md](reference.md)。

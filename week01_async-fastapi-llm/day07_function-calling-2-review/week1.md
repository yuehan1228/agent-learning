# 第 1 周复盘：从 LLM API 到工具调用 Agent

## 一、本周学习主线

本周围绕六条主线展开：环境与配置、异步并发、结构化输出、HTTP 服务、流式响应、工具调用。

| 天数 | 内容 | 对应练习 |
|---|---|---|
| Day 01 | 环境变量、LLM SDK、多轮消息与 token 用量 | `hello_llm.py` |
| Day 02 | 同步与异步请求、TaskGroup、耗时对比 | `bench_sync_vs_async.py` |
| Day 03 | Semaphore、超时、Pydantic 校验与重试 | `structured_output.py` |
| Day 04 | FastAPI 请求体、响应模型、Depends、lifespan | `app/main.py` |
| Day 05 | 流式事件、SSE、错误事件与结束标记 | `stream_response.py` |
| Day 06 | Function Calling 闭环、并行工具调用 | `tool_demo_1.py`、`tool_demo_parallel.py` |
| Day 07 | 工具注册表、错误回传与模型自我修正 | `tool_demo.py` |

> 以下数据来自此前实际检查与运行，不代表每次运行都会得到相同耗时。Day 07 问题记录以本次检查版本为准。

## 二、核心知识整理

### 1. 配置与多轮对话
- `load_dotenv` 将 `.env` 中的配置加载到环境变量；代码通过 `os.environ` 或 `os.getenv` 读取，并不是自动生成 Python 变量。
- `Path(__file__)` 可以基于脚本位置定位项目根目录，避免启动目录变化导致找不到 `.env`。
- API key 不写进源码，`.env` 不提交到 Git；`MODEL_NAME`、`API_BASE_URL` 也可以通过配置管理。
- 普通无状态调用需要显式传回历史消息。第二次请求想接着第一次聊，必须保留上下文，或使用 API 提供的会话关联机制。
- token 用量要覆盖所有调用；只打印最后一次请求的 usage 不等于整个任务总用量。

### 2. 异步并发与计时
- `async def` 定义协程函数；`await` 等待异步操作，等待期间事件循环可以调度其他任务。
- `TaskGroup` 和 `gather` 可以并发运行多个协程。异步适合网络 IO，不会自动加速 CPU 密集型计算。
- 在 `async def` 内调用同步 `OpenAI` 仍会阻塞事件循环，必须使用 `AsyncOpenAI` 并 `await`。
- 用 `time.perf_counter()` 的差值统计耗时，比打印时钟时间更准确。
- `TaskGroup` 中一个任务发生未处理异常时，通常会取消其余任务；需要逐任务容错时，应在合适边界处理异常。

Day 02 的 5 个独立问题，3 轮平均：

| 方式 | 平均耗时 |
|---|---|
| 同步串行 | 20.47 秒 |
| 异步并发 | 5.14 秒 |

加速比约 `20.4682 / 5.1444 = 3.98`。这只是一次小规模实验；固定先同步后异步，未交换顺序，也没有记录各轮波动。

### 3. 并发控制与超时
- `Semaphore(5)` 限制同时进入受保护区域的任务数量，不是限制总请求数，也不是每秒请求数限制。
- 单请求超时与整批总超时是两个层级：单个任务慢，不应无意中取消整批任务。
- Day 03 最初用 5 秒总超时包住 TaskGroup，只返回了 3 个结果；调整为单请求 60 秒、整批 120 秒后，10 个请求全部返回。

### 4. Pydantic：结构正确不等于事实正确
- 继承 `BaseModel` 定义字段类型，使用 `Field` 增加长度、范围等限制。
- `model_validate_json()` 同时完成 JSON 解析与模型校验；失败时可捕获 `ValidationError`。
- 校验失败后，将字段路径和原因回传给模型，要求修正，并设置重试上限。
- 输入只有 Alice，却要求至少 2 个参与者，模型可能用 `Unknown` 凑数；要求 5 人时，也曾返回 5 个重复的 Alice。
- `date: Date | None = None` 允许日期为 `null`。没有日期时填 `null` 比编造日期更合理。
- 规则和事实冲突时，不能指望重试创造缺失信息，应放宽不合理约束或向用户追问。

### 5. FastAPI：请求到模型再到响应
- 请求模型负责 JSON 入参校验；`response_model` 约束出参结构。Day 04 的接口约定是 `{"message": "..."}` → `{"reply": "..."}`。
- 普通的 `user_input: str` 路由参数默认可能被识别为 query 参数，不等于 JSON 请求体。
- `Depends` 注入客户端；`lifespan` 在启动时创建、退出时关闭客户端，复用连接。
- 缺字段或不满足模型约束时返回 422；上游 API 错误可转换成 502，避免暴露完整上游错误。
- 实测同步客户端会拖慢其他请求：修复后，并发聊天期间健康检查恢复为毫秒级响应。

### 6. SSE 流式输出
- LLM 设置 `stream=True`，按事件消费增量文本，再通过 `StreamingResponse` 转发。
- SSE 每条消息格式是 `data: <内容>\n\n`，媒体类型为 `text/event-stream`。
- 本项目事件约定：`delta` 为增量文本、`usage` 为 token 用量、`error` 为错误，`[DONE]` 为结束标记（大小写必须一致）。
- 流式响应头发出后，不能再把 HTTP 200 改成 502，因此客户端也要检查流内错误事件。
- 客户端断开时要释放上游连接；当前显式断开检测位于事件循环内，上游长期无事件时的资源释放仍需谨慎处理。
- 曾观察到上游事件集中到达。直接调用上游也出现类似现象，说明不能只凭 `stream=True` 保证明显的逐字效果；具体是否缓冲、模型是否推理等原因尚未单独验证。

## 三、工具调用：模型提议，应用执行

Responses API 中的基本流程：

```text
用户问题 + 工具 schema
    → 模型返回 function_call(name, arguments, call_id)
    → 应用解析参数、校验权限并执行工具
    → 回传 function_call_output(call_id, output)
    → 模型继续调用工具，或返回最终回答
```

- 模型不能直接执行本地函数，真正的权限和安全边界在应用代码中。
- Responses API 使用 `function_call` / `function_call_output`；Chat Completions 的 `tool_calls` / `tool` 消息是另一套消息格式，不应混用。
- 保留模型原始 `response.output`，包括可能存在的 reasoning 项，再追加工具结果。
- `call_id` 用来将工具结果对应到模型发出的调用。
- 注册表将工具名映射到 schema 和函数，避免为每个工具重复写调度分支。
- schema 的描述不等于本地校验：类型、范围、访问路径、允许的运算符仍需在执行前验证。
- 请求级并发和工具级并行不同：多个独立对话同时跑，不等于一次响应返回多个工具调用。
- Day 06 的 4 个模拟慢工具，每个等待 1 秒：串行约 4 秒，`gather` 并发约 1 秒。这是工具执行耗时，不包含模型请求时间。

## 四、Day 07 错误恢复实测

使用 scratch 临时文本文件，不读取私人文件。要求模型先计算 `1/0`，看到错误后改为 `2**10`，并读取临时文件第 1–2 行。

```text
第 1 轮调用 calculator：{"expression": "1/0"}
第 1 轮结果：Error: ZeroDivisionError: division by zero

第 1 轮调用 read_local_file：传入临时路径、start_line=1、end_line=2、encoding=utf-8
第 1 轮结果：1: first\n2: second

第 2 轮调用 calculator：{"expression": "2**10"}
第 2 轮结果：1024

最终回答：说明除零错误及修正结果，并给出文件内容。
```

这验证了“错误作为工具结果回传 → 模型修正参数 → 再次调用 → 最终回答”的完整闭环。未知工具也能返回错误结果，而不是直接崩溃。

### 容易误判的例子：`2^10`

实测 `simple_eval("2^10")` 返回 **8**，不是异常。Python 中 `^` 是按位异或，`**` 才是幂运算。因此原先用 `2^10` 制造错误的实验不可靠：工具返回数值不代表数值符合用户意图。

## 五、Day 07 待完善项（检查时尚未修复）

- [ ] 为文件读取实现真正的默认参数。目前只传 `file_path` 时，行号参数为 `None`，会触发比较运算 `TypeError`。
- [ ] 校验 `start_line >= 1`、`end_line >= start_line`，并设置读取长度上限。目前结束行小于起始行会静默返回空文本。
- [ ] 文件读取限制在专门的练习数据目录内；解析 `..`、绝对路径和符号链接后再检查边界，避免读取 `.env` 等敏感文件。
- [ ] 对计算器允许的运算符进行本地约束，或明确拒绝 `^`，避免异或被误当成幂运算。
- [ ] 将 Day 06 的 `get_weather` 接入同一注册表，满足“3 个工具齐全的小 Agent”。当前只有计算器和文件读取两个工具。

## 六、自测与下周衔接

尝试不看代码回答：
1. 为什么把同步 SDK 放进 `async def` 仍然会阻塞？
async def 只是把函数声明为协程（Coroutine），并不会自动将其内部的代码改造成非阻塞执行。
2. 总超时和单请求超时的区别是什么？
单请求超时（Per-request Timeout）：针对某一次独立网络调用的时间上限（例如单次调用大模型推理或搜索 API 最多等 15 秒）。总超时（Total / End-to-End Timeout）：针对整个业务请求生命周期的全局时间预算。
3. 为什么 Pydantic 校验通过后仍可能出现幻觉？
Pydantic 校验的是语法与结构合规性（Syntactic & Type Validity），而不是事实真实性（Semantic Truthfulness）。
4. 为什么流式接口出错时可能仍返回 HTTP 200？
这是由 HTTP 协议的传输时序决定的：HTTP 状态码位于响应头（Response Headers）的最前端，必须在发送任何响应体（Response Body）之前确定并刷出给客户端。
5. `call_id` 有什么作用？模型返回多个调用时如何执行并回传？
作为唯一关联标识（Correlation ID），将模型的单次调用指令与本地工具的执行结果精确绑定。
6. 工具 schema 为什么不能替代本地参数校验和权限控制？

下周将补 PostgreSQL、Docker、Redis 和会话持久化，再把当前工具循环接入服务。优先完成上面的安全与默认参数问题，不急于增加更多工具或框架。

# Day 03 笔记：并发控制 + Pydantic 结构化输出

## 1. Semaphore 限流 + 超时（10 个请求，`Semaphore(5)`）
- 改动前：用 `asyncio.timeout(5)` 包住整个 TaskGroup，是**总超时**，10 个请求只完成 3 个，其余被取消。
- 改动后：单请求超时 `wait_for(..., 60s)`，整批总超时 120s 仅作兜底；超时的请求只记录序号，不影响其他请求。
- 结果：10 个请求全部返回，`超时失败的请求序号: 无`。

## 2. 结构化输出 + 校验重试

### 为什么要改 schema 与 prompt
第一版里，输入只有 "Alice are going to a science fair"，模型为满足 `min_length=2` 和必填 date：
- 编造了日期 `2024-01-01`
- 编造了参与者 `"Unknown"`

校验能通过，但数据是假的。因此把 `date` 改为可选，并在 prompt 里要求"信息缺失时填 null、不要编造"。

### 失败重试日志（故意把参与者要求改成恰好 5 人，制造校验失败）
```
raw_text: {"name":"science fair","participants":["Alice"],"date":null}
[第 1 次校验失败]：[{'type': 'too_short', 'loc': ('participants',),
   'msg': 'List should have at least 5 items after validation, not 1',
   'ctx': {'min_length': 5, 'actual_length': 1}}]
raw_text: {"name":"science fair","participants":["Alice","Alice","Alice","Alice","Alice"],"date":null}
结果: name='science fair' date=None participants=['Alice' x5]
```
- 第 1 次失败，把简化后的错误（字段路径 + 原因）回传给模型，第 2 次通过。
- 回传内容由原来的 `err.json()` 精简为 `- participants: List should have at least 5 items...`。

## 3. 结论
1. 重试闭环有效：ValidationError 文本交给模型，模型能按错误修正格式。
2. **校验通过 ≠ 数据正确**：模型会为了通过校验而凑数（"Unknown"、重复的 "Alice"）。结构校验只保证格式，不保证语义，业务上还需要语义校验（如参与者去重），或者允许字段为空。
3. 超时要区分"单请求超时"和"整批总超时"，否则一个慢请求会拖垮全部。

## 4. 本次修改的小问题
- `attemp` 拼写改为 `attempt`
- 删除不会执行的 `raise RuntimeError`（已由用户先行删除）
- 回传的错误信息精简
- 模型名改为读取环境变量 `MODEL_NAME`（未设置时用默认值）

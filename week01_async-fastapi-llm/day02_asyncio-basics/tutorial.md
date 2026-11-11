# Day 02 · asyncio 基础

> 11/12（周二） · 建议时长 1.5h · 第 1 周

## 今日目标
理解事件循环与协程，并量化并发带来的收益。

## 衔接
- 前一天：环境与仓库
- 后一天：asyncio 进阶 + Pydantic

## 学习内容
- `async/await`、协程与事件循环
- `asyncio.run`、`create_task`、`gather`
- IO 密集 vs CPU 密集：为什么异步适合调用 LLM

## 学习资料（按顺序学习）

| 学习点 | 资料 | 读哪部分 | 预计 |
|---|---|---|---|
| 协程与事件循环 | [廖雪峰：asyncio（中文，入门首选）](https://liaoxuefeng.com/books/python/async-io/asyncio/index.html) | 通读，先建立直观印象 | 20 min |
| create_task / gather | [Python 官方：Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html) | 读 Coroutines、Creating Tasks、Running Tasks Concurrently | 30 min |
| 异步 SDK | [openai-python：Async usage](https://github.com/openai/openai-python) | 找到 AsyncOpenAI 的示例，照着写 | 10 min |

> 更多概念与延伸阅读见 [reference.md](reference.md)。先读资料再动手，卡住时回到对应小节。

## 练习步骤
1. 用 `AsyncOpenAI` 并发请求 5 次 LLM
2. 实现同步版本，对比两者耗时
3. 用 `time.perf_counter` 记录并整理成表格

## 今日产出
- [ ] `bench_sync_vs_async.py`
- [ ] 在笔记中记录耗时对比数据与结论

## 自测
- 不看资料，能否口述今天的核心流程？
- 遇到卡点超过 30 分钟：先保留产出，砍掉拓展内容，不顺延。

## 备注
进阶提示：`asyncio.TaskGroup`（3.11+）提供结构化并发，可作为 gather 的替代。

参考资料见同目录 [reference.md](reference.md)。

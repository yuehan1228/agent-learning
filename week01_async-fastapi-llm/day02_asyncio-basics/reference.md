# Day 02 · asyncio 基础 · 参考资料

## 关键概念
- **协程**：用 async def 定义，调用后返回协程对象，需 await 或交给事件循环。
- **事件循环**：单线程内调度协程，遇到 await 让出控制权。
- **gather**：并发运行多个可等待对象并按序收集结果。
- **阻塞调用**：在协程中调用 time.sleep 或同步 SDK 会卡住整个循环。

## 参考与延伸阅读
- Python 官方 asyncio 文档 https://docs.python.org/3/library/asyncio.html
- Real Python: Async IO in Python
- Python 3.11 TaskGroup 简介

## 补充说明
进阶提示：`asyncio.TaskGroup`（3.11+）提供结构化并发，可作为 gather 的替代。

返回教学文档：[tutorial.md](tutorial.md)

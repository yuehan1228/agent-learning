# Day 13 · Agent 循环完善 + 可观测雏形

> 11/23（周六） · 建议时长 3.75h · 第 2 周

## 今日目标
让 Agent 具备基本鲁棒性，并开始用数据评估它。

## 衔接
- 前一天：Agent 循环（ReAct 雏形）
- 后一天：阶段整合 + 复盘

## 学习内容
- 超时、重试、指数退避
- 结构化日志
- 最小评测思维

## 学习资料（按顺序学习）

| 学习点 | 资料 | 读哪部分 | 预计 |
|---|---|---|---|
| 重试 | [tenacity 文档](https://tenacity.readthedocs.io/en/latest/) | 读 Basic Retry、Wait、Stop | 15 min |
| 结构化日志 | [structlog：Getting Started](https://www.structlog.org/en/stable/getting-started.html) | 跟着做一遍 | 15 min |
| 超时 | [Python 官方：Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html) | 复习 Timeouts | 5 min |
| 评测思维 | [Anthropic：Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | 重读 Agent 失败与调试相关段落 | 10 min |

> 更多概念与延伸阅读见 [reference.md](reference.md)。先读资料再动手，卡住时回到对应小节。

## 练习步骤
1. 为 LLM 与工具调用加超时和重试（tenacity 或手写）
2. 每步记录 JSON 日志：输入、输出、耗时、token
3. 将 Agent 接入 FastAPI，用 SSE 流式输出每一步状态
4. 设计 5 个测试问题，手工标注成功或失败并计算成功率

## 今日产出
- [ ] 带日志的 Agent 服务
- [ ] `eval_v0.md`：5 题结果与失败原因

## 自测
- 不看资料，能否口述今天的核心流程？
- 遇到卡点超过 30 分钟：先保留产出，砍掉拓展内容，不顺延。

## 备注
你的感知算法背景在这里有优势：用评测指标驱动迭代，而不是凭感觉。

参考资料见同目录 [reference.md](reference.md)。

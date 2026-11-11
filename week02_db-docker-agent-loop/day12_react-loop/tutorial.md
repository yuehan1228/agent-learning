# Day 12 · Agent 循环（ReAct 雏形）

> 11/22（周五） · 建议时长 1.5h · 第 2 周

## 今日目标
手写思考—行动—观察循环。

## 衔接
- 前一天：对话持久化
- 后一天：Agent 循环完善 + 可观测雏形

## 学习内容
- ReAct 论文的核心思想
- 循环终止条件：最终回答或达到最大步数

## 学习资料（按顺序学习）

| 学习点 | 资料 | 读哪部分 | 预计 |
|---|---|---|---|
| ReAct 论文 | [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629) | 读 Abstract、Introduction、Section 2 方法 | 40 min |
| Agent 设计总览 | [Anthropic：Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | 通读，重点看 Agents 一节 | 30 min |
| 补充综述 | [Lilian Weng：LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) | 读 Planning 与 Tool Use，选读 | 20 min |

> 更多概念与延伸阅读见 [reference.md](reference.md)。先读资料再动手，卡住时回到对应小节。

## 练习步骤
1. 阅读 ReAct 摘要与方法部分（约 1 小时）
2. 用 `while step < max_steps` 实现循环，复用第 1 周工具注册表
3. 当模型不再返回 tool_calls 时视为结束
4. 打印每一步的决策

## 今日产出
- [ ] `agent_loop.py` 初版

## 自测
- 不看资料，能否口述今天的核心流程？
- 遇到卡点超过 30 分钟：先保留产出，砍掉拓展内容，不顺延。

## 备注
对比：原论文用文本解析 Thought/Action，现代做法用原生 tool calling，更稳健。

参考资料见同目录 [reference.md](reference.md)。

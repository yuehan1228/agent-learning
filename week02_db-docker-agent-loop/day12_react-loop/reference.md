# Day 12 · Agent 循环（ReAct 雏形） · 参考资料

## 关键概念
- **ReAct**：Reasoning + Acting：推理与行动交替，用观察修正后续推理。
- **max_steps**：防止无限循环和费用失控的硬性保护。
- **停止条件**：没有 tool_calls 即最终答案。

## 参考与延伸阅读
- ReAct 论文 https://arxiv.org/abs/2210.03629
- Anthropic: Building effective agents https://www.anthropic.com/engineering/building-effective-agents
- Lilian Weng: LLM Powered Autonomous Agents

## 补充说明
对比：原论文用文本解析 Thought/Action，现代做法用原生 tool calling，更稳健。

返回教学文档：[tutorial.md](tutorial.md)

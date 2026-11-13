# Day 06 · Function Calling（上）

> 11/16（周六） · 建议时长 3.75h · 第 1 周

## 今日目标
不借助框架，完整跑通一次工具调用闭环。

## 衔接
- 前一天：流式输出
- 后一天：Function Calling（下）+ 周复盘

## 学习内容
- tools 参数与 JSON Schema 描述
- `tool_calls` 响应结构、`tool` 角色消息
- 工具调用闭环与并行调用

## 学习资料（按顺序学习）

| 学习点 | 资料 | 读哪部分 | 预计 |
|---|---|---|---|
| Function Calling 全流程 | [OpenAI：Function calling](https://platform.openai.com/docs/guides/function-calling) | 通读，重点看完整调用流程示意 | 40 min |
| 国内模型写法 | [DeepSeek：Function Calling](https://api-docs.deepseek.com/guides/function_calling) | 对照自己用的模型看示例 | 15 min |
| 另一家视角 | [Anthropic：Tool use overview](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview) | 对比 tool_use 与 tool_result 的设计 | 20 min |
| JSON Schema | [JSON Schema：Getting started](https://json-schema.org/learn/getting-started-step-by-step) | 读到 properties 与 required | 20 min |

> 更多概念与延伸阅读见 [reference.md](reference.md)。先读资料再动手，卡住时回到对应小节。

## 练习步骤
1. 阅读 OpenAI function calling 文档并画出时序图
2. 实现 `get_weather`（可用假数据或公开 API）
3. 手写闭环：请求 → 模型返回 tool_calls → 本地执行 → 回传结果 → 最终回答
4. 让模型一次发起多个并行调用并全部处理

## 今日产出
- [x] `tool_demo_1.py`（并行演示见 `tool_demo_parallel.py`）
- [x] 时序图（Mermaid 或手绘）（见 [notes.md](notes.md)）

## 自测
- 不看资料，能否口述今天的核心流程？
- 遇到卡点超过 30 分钟：先保留产出，砍掉拓展内容，不顺延。

## 备注
思考：模型只“提议”调用，真正执行在你的代码里，这是安全边界的所在。

参考资料见同目录 [reference.md](reference.md)。

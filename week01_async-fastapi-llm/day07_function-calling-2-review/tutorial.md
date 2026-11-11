# Day 07 · Function Calling（下）+ 周复盘

> 11/17（周日） · 建议时长 3.75h · 第 1 周

## 今日目标
扩充工具集，学会处理错误，并完成第 1 周复盘。

## 衔接
- 前一天：Function Calling（上）
- 后一天：PostgreSQL 基础

## 学习内容
- 工具注册表模式
- 工具错误回传与模型自我修正
- 参数校验

## 学习资料（按顺序学习）

| 学习点 | 资料 | 读哪部分 | 预计 |
|---|---|---|---|
| 工具设计 | [Anthropic：Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | 通读，关注工具描述与错误信息的写法 | 30 min |
| Function Calling 复习 | [OpenAI：Function calling](https://platform.openai.com/docs/guides/function-calling) | 重读 Handling function calls 部分 | 15 min |
| JSON Schema | [JSON Schema：Getting started](https://json-schema.org/learn/getting-started-step-by-step) | 复习，写校验规则时使用 | 10 min |

> 更多概念与延伸阅读见 [reference.md](reference.md)。先读资料再动手，卡住时回到对应小节。

## 练习步骤
1. 新增计算器和读本地文件（或网页搜索）两个工具
2. 用注册表（dict）统一管理 schema 与函数
3. 故意让工具抛错，把错误文本回传，观察模型是否修正
4. 复盘 1 小时：整理笔记、提交代码

## 今日产出
- [ ] 3 个工具齐全的小 Agent
- [ ] `week1.md` 学习笔记

## 自测
- 不看资料，能否口述今天的核心流程？
- 遇到卡点超过 30 分钟：先保留产出，砍掉拓展内容，不顺延。

## 备注
周检查点：能否不看文档独立写出完整的工具调用闭环？不能就重做 day06。

参考资料见同目录 [reference.md](reference.md)。

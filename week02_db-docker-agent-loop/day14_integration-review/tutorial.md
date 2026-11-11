# Day 14 · 阶段整合 + 复盘

> 11/24（周日） · 建议时长 3.75h · 第 2 周

## 今日目标
完成里程碑 1：可演示的迷你 Agent 服务。

## 衔接
- 前一天：Agent 循环完善 + 可观测雏形
- 后一天：第 3 周：最小 RAG

## 学习内容
- 项目文档化
- Mermaid 架构图
- RAG 预习：Embedding 与向量检索

## 学习资料（按顺序学习）

| 学习点 | 资料 | 读哪部分 | 预计 |
|---|---|---|---|
| 架构图 | [Mermaid：About](https://mermaid.js.org/intro/) | 读 flowchart 与 sequenceDiagram 语法 | 20 min |
| Embedding 直觉 | [Jay Alammar：The Illustrated Word2vec](https://jalammar.github.io/illustrated-word2vec/) | 通读，图解为主 | 30 min |
| Embedding 接口 | [OpenAI：Embeddings](https://platform.openai.com/docs/guides/embeddings) | 读概念与示例，了解余弦相似度 | 15 min |
| 向量库预习 | [pgvector README](https://github.com/pgvector/pgvector) | 读 Getting Started 与 Querying | 15 min |

> 更多概念与延伸阅读见 [reference.md](reference.md)。先读资料再动手，卡住时回到对应小节。

## 练习步骤
1. 整合：Agent 循环 + 3 个工具 + Postgres 持久化 + compose 一键启动
2. 编写 README：架构图、启动方法、示例请求
3. 从零 clone 后按 README 验证可启动
4. 阅读 1 篇 Embedding 与向量检索文章，写 `week2.md` 复盘

## 今日产出
- [ ] 里程碑 1 仓库
- [ ] README 与架构图
- [ ] `week2.md`

## 自测
- 不看资料，能否口述今天的核心流程？
- 遇到卡点超过 30 分钟：先保留产出，砍掉拓展内容，不顺延。

## 备注
下一步：第 3–4 周将手写最小 RAG，并建立 50 条评测集。

参考资料见同目录 [reference.md](reference.md)。

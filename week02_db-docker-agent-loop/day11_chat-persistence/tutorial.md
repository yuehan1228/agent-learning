# Day 11 · 对话持久化

> 11/21（周四） · 建议时长 1.5h · 第 2 周

## 今日目标
让服务支持多轮、可恢复的会话。

## 衔接
- 前一天：docker-compose + Redis
- 后一天：Agent 循环（ReAct 雏形）

## 学习内容
- session_id 设计
- 读写路径：Postgres 为权威存储，Redis 为热缓存
- 上下文窗口与滑动窗口截断

## 学习资料（按顺序学习）

| 学习点 | 资料 | 读哪部分 | 预计 |
|---|---|---|---|
| Token 计数 | [tiktoken README](https://github.com/openai/tiktoken) | 读 Usage 示例 | 10 min |
| 上下文管理思路 | [Anthropic：Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 通读，关注 context 的取舍 | 30 min |
| 缓存与数据库读写 | [redis-py 文档](https://redis-py.readthedocs.io/en/stable/) | 复习 expire / lrange | 10 min |

> 更多概念与延伸阅读见 [reference.md](reference.md)。先读资料再动手，卡住时回到对应小节。

## 练习步骤
1. `/chat` 增加 `session_id`，缺省则新建
2. 先查 Redis，未命中则回源 Postgres
3. 取最近 N 条或按 token 估算做截断
4. 重启服务后验证对话仍可继续

## 今日产出
- [ ] 多轮、可恢复的对话服务

## 自测
- 不看资料，能否口述今天的核心流程？
- 遇到卡点超过 30 分钟：先保留产出，砍掉拓展内容，不顺延。

## 备注
展望：滑动窗口会丢失早期信息，后续可以引入摘要和长期记忆。

参考资料见同目录 [reference.md](reference.md)。

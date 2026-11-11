# Day 11 · 对话持久化 · 参考资料

## 关键概念
- **上下文窗口**：模型一次可处理的 token 上限，超出会报错或遗忘。
- **缓存一致性**：写入时同时更新两处，并以数据库为准。
- **截断策略**：固定条数、按 token、摘要压缩，难度递增。

## 参考与延伸阅读
- tiktoken 项目
- Anthropic: Effective context engineering（博客）

## 补充说明
展望：滑动窗口会丢失早期信息，后续可以引入摘要和长期记忆。

返回教学文档：[tutorial.md](tutorial.md)

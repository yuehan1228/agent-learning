# Day 01 · 环境与仓库 · 参考资料

## 关键概念
- **OpenAI 兼容接口**：多数国内模型提供与 OpenAI SDK 一致的协议，只需改 base_url 与 model。
- **messages**：由 role(system/user/assistant) 与 content 构成的对话列表，模型无状态，历史需自己传。
- **temperature**：采样随机性，调试时可设 0 以便复现。
- **usage**：响应中的 prompt/completion token 数，是成本监控的基础。

## 参考与延伸阅读
- DeepSeek API 文档 https://api-docs.deepseek.com
- 通义千问 DashScope 兼容模式文档
- OpenAI Python SDK README https://github.com/openai/openai-python
- uv 文档 https://docs.astral.sh/uv/

## 补充说明
常见问题：401 多为 key 错误或未加载 .env；超时可检查网络或代理。

返回教学文档：[tutorial.md](tutorial.md)

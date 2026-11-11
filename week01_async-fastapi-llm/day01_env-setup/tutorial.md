# Day 01 · 环境与仓库

> 11/11（周一） · 建议时长 1.5h · 第 1 周

## 今日目标
搭好开发环境并用代码完成第一次 LLM 调用。

## 衔接
- 前一天：无（起点）
- 后一天：asyncio 基础

## 学习内容
- Python 3.11+ 虚拟环境管理（uv 或 conda）
- OpenAI 兼容接口的概念：base_url、api_key、model
- 用 .env 管理密钥，避免提交到 Git

## 学习资料（按顺序学习）

| 学习点 | 资料 | 读哪部分 | 预计 |
|---|---|---|---|
| Python 环境管理（uv） | [uv 官方：Working on projects](https://docs.astral.sh/uv/guides/projects/) | 读 Creating projects、Managing dependencies 两节 | 15 min |
| OpenAI 兼容接口 | [DeepSeek API 文档（首页 Quick Start）](https://api-docs.deepseek.com/) | 看 base_url、model 与第一次调用示例 | 10 min |
| OpenAI 兼容接口（备选） | [阿里云百炼：OpenAI 兼容调用（中文）](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope) | 用 Qwen 的同学读此篇 | 10 min |
| SDK 用法 | [openai-python README](https://github.com/openai/openai-python) | 读 Usage、Async usage | 15 min |
| 文本生成与 messages | [OpenAI：Text generation](https://platform.openai.com/docs/guides/text) | 理解 role 与多轮消息 | 15 min |
| 密钥管理 | [python-dotenv README](https://github.com/theskumar/python-dotenv) | 读 Getting Started | 5 min |
| 忽略文件 | [Git：gitignore 文档](https://git-scm.com/docs/gitignore) | 读 Pattern Format 前半部分 | 5 min |

> 更多概念与延伸阅读见 [reference.md](reference.md)。先读资料再动手，卡住时回到对应小节。

## 练习步骤
1. 安装 Python 3.11+、uv（或 conda）、VS Code
2. 注册 DeepSeek 或 Qwen API 并小额充值（10–20 元）
3. `uv add openai python-dotenv`，把 key 写入 `.env`，并把 `.env` 加入 `.gitignore`
4. 编写 `hello_llm.py`：发送一条消息并打印回复、token 用量

## 今日产出
- [ ] `hello_llm.py` 可运行并已提交
- [ ] `.gitignore` 已忽略 `.env`

## 自测
- 不看资料，能否口述今天的核心流程？
- 遇到卡点超过 30 分钟：先保留产出，砍掉拓展内容，不顺延。

## 备注
常见问题：401 多为 key 错误或未加载 .env；超时可检查网络或代理。

参考资料见同目录 [reference.md](reference.md)。

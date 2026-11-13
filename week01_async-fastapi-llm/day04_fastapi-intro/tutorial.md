# Day 04 · FastAPI 入门

> 11/14（周四） · 建议时长 1.5h · 第 1 周

## 今日目标
用 FastAPI 把 LLM 调用封装成可调用的 HTTP 服务。

## 衔接
- 前一天：asyncio 进阶 + Pydantic
- 后一天：流式输出

## 学习内容
- 路由、请求体与响应模型
- 依赖注入 `Depends`
- 自动文档 `/docs`

## 学习资料（按顺序学习）

| 学习点 | 资料 | 读哪部分 | 预计 |
|---|---|---|---|
| 路由与第一个接口 | [FastAPI 教程：First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/) | 跟着敲一遍 | 15 min |
| 请求体 | [FastAPI 教程：Request Body](https://fastapi.tiangolo.com/tutorial/body/) | 通读并实践 | 20 min |
| 依赖注入 | [FastAPI 教程：Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) | 读第一篇即可 | 15 min |
| 中文版目录 | [FastAPI 中文教程](https://fastapi.tiangolo.com/zh/tutorial/) | 英文吃力时对照阅读 | — |

> 更多概念与延伸阅读见 [reference.md](reference.md)。先读资料再动手，卡住时回到对应小节。

## 练习步骤
1. `uv add fastapi uvicorn`
2. 编写 `POST /chat`：接收 message，调用 LLM 返回回复
3. 用 Pydantic 定义请求与响应模型
4. 在 Swagger 页面完成调用，并加 `/health` 接口

## 今日产出
- [x] 可运行的 `app/main.py`
- [x] Swagger 页面调用成功的截图或记录（见 [notes.md](notes.md)）

## 自测
- 不看资料，能否口述今天的核心流程？
- 遇到卡点超过 30 分钟：先保留产出，砍掉拓展内容，不顺延。

## 备注
提示：把 AsyncOpenAI 客户端放到启动阶段创建，不要每次请求新建。

参考资料见同目录 [reference.md](reference.md)。

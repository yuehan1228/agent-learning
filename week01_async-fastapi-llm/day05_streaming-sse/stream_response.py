from contextlib import asynccontextmanager
import json
from typing import Annotated

from fastapi import FastAPI, Request, Depends
import logging
import asyncio
from openai import AsyncOpenAI, OpenAI
from pathlib import Path
import os
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

logger = logging.getLogger("uvicorn.error")
load_dotenv(Path(__file__).parent.parent.parent / ".env")

MODEL = os.environ["MODEL_NAME"]

def print_chunk():
    client = OpenAI(base_url=os.environ["API_BASE_URL"], api_key=os.environ["OPENAI_API_KEY"])

    input_list = [
        {"role": "system", "content": "You are a helpful assistant and answer with Chinese."},
        {"role": "user", "content": "请用一句话解释递归"}
    ]

    stream = client.responses.create(
        model=MODEL,
        input=input_list,
        stream=True
    )

    for i, event in enumerate(stream):
        if (event.type == "response.output_text.delta"):
            print(f"{i}: {event.delta}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.llm = AsyncOpenAI(base_url=os.environ["API_BASE_URL"], api_key=os.environ["OPENAI_API_KEY"])
    app.state.sem = asyncio.Semaphore(5)
    yield
    await app.state.llm.close()

async def get_llm(request: Request):
    return request.app.state.llm

async def get_sem(request: Request):
    return request.app.state.sem

LLMClient = Annotated[AsyncOpenAI, Depends(get_llm)]
SemClient = Annotated[asyncio.Semaphore, Depends(get_sem)]

app = FastAPI(lifespan=lifespan)

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, description="用户输入")

@app.post("/chat/stream", response_class=StreamingResponse, tags=["Chat"])
async def chat(request: Request, req: ChatRequest, llm: LLMClient, sem: SemClient):
    input_list = [
        {"role": "system", "content": "You are a helpful assistant and answer with Chinese."},
        {"role": "user", "content": req.message}
    ]
    
    async def generate():
        try:
            async with sem:
                stream = await llm.responses.create(
                    model=MODEL,
                    input=input_list,
                    stream=True
                )

                async for event in stream:
                    # 客户端已断开：停止消费，关闭上游连接，避免浪费 token
                    if await request.is_disconnected():
                        await stream.close()
                        return

                    if event.type == "response.output_text.delta":
                        data = json.dumps(
                            {"type": "delta", "content": event.delta},
                            ensure_ascii=False,
                        )
                        yield f"data: {data}\n\n"

                    elif event.type == "response.completed" and event.response.usage:
                        usage = json.dumps(
                            {"type": "usage", "usage": event.response.usage.total_tokens},
                            ensure_ascii=False,
                        )
                        yield f"data: {usage}\n\n"

        except Exception as e:
            # 详细错误只写日志，不把上游原始信息返回给调用方
            logger.exception("stream failed")
            err_data = json.dumps(
                {"type": "error", "message": f"LLM 调用失败: {type(e).__name__}"},
                ensure_ascii=False,
            )
            yield f"data: {err_data}\n\n"

        # 正常结束或出错都以 [DONE] 收尾（客户端断开时已提前 return）
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )

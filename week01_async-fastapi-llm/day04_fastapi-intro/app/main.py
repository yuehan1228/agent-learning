import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from openai import APIError, AsyncOpenAI
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).parent.parent.parent.parent / ".env")
MODEL = os.environ["MODEL_NAME"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动阶段创建一次客户端，所有请求复用
    app.state.llm = AsyncOpenAI(base_url=os.environ["API_BASE_URL"], api_key=os.environ["OPENAI_API_KEY"])
    yield
    await app.state.llm.close()


def get_llm(request: Request) -> AsyncOpenAI:
    return request.app.state.llm


LLMClient = Annotated[AsyncOpenAI, Depends(get_llm)]

app = FastAPI(lifespan=lifespan)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, description="用户消息")


class ChatResponse(BaseModel):
    reply: str


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(req: ChatRequest, llm: LLMClient):
    input_list = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": req.message},
    ]
    try:
        response = await llm.responses.create(model=MODEL, input=input_list)
    except APIError as e:
        # 上游模型出错：返回 502，而不是让服务抛 500
        raise HTTPException(status_code=502, detail=f"LLM 调用失败: {type(e).__name__}")
    return ChatResponse(reply=response.output_text)

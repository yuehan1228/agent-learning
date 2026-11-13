import os
from pathlib import Path
from typing import Annotated
from fastapi import FastAPI, Request, Depends, HTTPException
from openai import AsyncOpenAI, APIError
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field
import asyncio

load_dotenv(Path(__file__).parent.parent.parent.parent / ".env")
model = os.environ["MODEL_NAME"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.llm = AsyncOpenAI(base_url=os.environ["API_BASE_URL"], api_key=os.environ["OPENAI_API_KEY"])
    app.state.semaphore = asyncio.Semaphore(5)
    yield
    await app.state.llm.close()
    
def get_llm(request: Request) -> AsyncOpenAI:
    return request.app.state.llm

def get_semaphore(request: Request) -> asyncio.Semaphore:
    return request.app.state.semaphore

LLMClient = Annotated[AsyncOpenAI, Depends(get_llm)]
SemClient = Annotated[asyncio.Semaphore, Depends(get_semaphore)]

app = FastAPI(lifespan=lifespan)

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, description="请求输入")

class ChatResponse(BaseModel):
    reply: str
    
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(req: ChatRequest, llm: LLMClient, sem: SemClient):
    input_list = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": req.message}
    ]
    
    async with sem:
        try:
            response = await llm.responses.create(
                model=model,
                input=input_list
            )
        except APIError as e:
            raise HTTPException(status_code=502, detail=f"LLM 调用失败: {type(e).__name__}")
        return ChatResponse(reply=response.output_text)
    
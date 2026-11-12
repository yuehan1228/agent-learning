import os
import time
import asyncio
from openai import OpenAI, AsyncOpenAI
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError, Field
import json
from datetime import date as Date

load_dotenv(Path(__file__).parent.parent.parent / ".env")

async_client = AsyncOpenAI(base_url=os.environ["API_BASE_URL"], api_key=os.environ["OPENAI_API_KEY"])
sync_client = OpenAI(base_url=os.environ["API_BASE_URL"], api_key=os.environ["OPENAI_API_KEY"])
MODEL = os.getenv("MODEL_NAME", "gemini-3.8-flash-high")
REQUEST_TIMEOUT = 10  # 单个请求超时（秒）
TOTAL_TIMEOUT = 20  # 整批请求总超时（秒）

async def get_responses(i, input_list, sem, failed):
    async with sem:
        try:
            response = await asyncio.wait_for(
                async_client.responses.create(model=MODEL, input=input_list),
                timeout=REQUEST_TIMEOUT,
            )
            print(f"Response: {i}, {response.output_text}")
        except asyncio.TimeoutError:
            failed.append(i)  # 单个请求超时只记录，不影响其他请求
            print(f"Response: {i} 超时（>{REQUEST_TIMEOUT}s）")
    
async def async_get_responses(system_prompt, inputs):    
    # Use asyncio.TaskGroup to run multiple tasks concurrently
    sem = asyncio.Semaphore(5)
    failed = []
    try:
        async with asyncio.timeout(TOTAL_TIMEOUT):
            async with asyncio.TaskGroup() as tg:
                for i, user_input in enumerate(inputs):
                    input_list = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ]
                    tg.create_task(get_responses(i + 1, input_list, sem, failed))
    except TimeoutError:
        print("整批请求总超时，未完成的请求已被取消。")
    print(f"超时失败的请求序号: {failed or '无'}")

def async_advanced():
    system_prompt = "You are a helpful coding assistant. Please answer in Chinese."
    inputs = [
        "请用一句话解释什么是递归？",
        "请用一句话解释什么是闭包？",
        "请用一句话解释什么是装饰器？",
        "请用一句话解释什么是生成器？",
        "请用一句话解释什么是协程？",
        "请用一句话解释什么是模板？",
        "请用一句话解释什么是依赖注入？",
        "请用一句话解释什么是单例模式？",
        "请用一句话解释什么是工厂模式？",
        "请用一句话解释什么是冒泡算法？"
    ]
    
    asyncio.run(async_get_responses(system_prompt, inputs))
            
class CalendarEvent(BaseModel):
    name: str = Field(description="活动名称，必填")
    date: Date | None = Field(default=None, description="活动日期，格式 YYYY-MM-DD；输入中没有明确日期时必须为 null，不要编造")
    participants: list[str] = Field(min_length=5, description="至少两个参与者")
    
def extract_event_with_retry(max_retries: int = 3) -> CalendarEvent:
    input_list = [
        {"role": "system", "content": "请从用户输入中提取日程活动信息。信息缺失时不要编造：date 填 null，参与者只写输入中出现的人名。"},
        {"role": "user", "content": "Alice are going to a science fair"},
    ]
    
    for attempt in range(max_retries):
        response = sync_client.responses.create(
            model=MODEL,
            input=input_list,
            text={
                    "format": {
                        "type": "json_schema",
                        "name": "CalendarEvent",
                        "schema": CalendarEvent.model_json_schema(),
                    },
                },
        )
        
        raw_text = response.output_text
        print(f"raw_text: {raw_text}")
        
        try:
            return CalendarEvent.model_validate_json(raw_text)
        except ValidationError as err:
            print(f"[第 {attempt + 1} 次校验失败]：{err.errors()}")
            if attempt == max_retries - 1:
                raise # 超出最大重试次数抛出异常
            
            errors = "\n".join(f"- {'.'.join(map(str, e['loc']))}: {e['msg']}" for e in err.errors())
            input_list.append({"role": "assistant", "content": raw_text})
            input_list.append({"role": "user", "content": f"你的输出未能通过校验，请修正后重新输出完整 JSON。错误：\n{errors}"})


if __name__ == "__main__":
    # async_advanced()
    # extract_event_with_retry()
    print(CalendarEvent.model_json_schema())

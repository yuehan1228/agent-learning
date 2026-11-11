import os
from pathlib import Path
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
import asyncio
import time

load_dotenv(Path(__file__).parent.parent.parent / ".env")

async_client = AsyncOpenAI(base_url=os.environ["API_BASE_URL"], api_key=os.environ["OPENAI_API_KEY"])
sync_client = OpenAI(base_url=os.environ["API_BASE_URL"], api_key=os.environ["OPENAI_API_KEY"])
GEMINI_MODEL = "gemini-3.8-flash-high"

def sync_get_chat_completions(system_prompt, messages):
    for i, user_input in enumerate(messages):
        message = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        response = sync_client.chat.completions.create(
            model=GEMINI_MODEL,
            messages=message,
            reasoning_effort="low"
        )
        print(f"Response {i + 1}, {response.choices[0].message.content}")
        
async def get_chat_completions(i, message):
    response = await async_client.chat.completions.create(
        model=GEMINI_MODEL,
        messages=message,
        reasoning_effort="high"
    )
    print(f"Response {i}, {response.choices[0].message.content}")

async def async_get_chat_completions(system_prompt, messages):
    # TaskGroup
    # async with asyncio.TaskGroup() as tg:
    #     for i, user_input in enumerate(messages):
    #         message = [
    #             {"role": "system", "content": system_prompt},
    #             {"role": "user", "content": user_input}
    #         ]
    #         tg.create_task(get_chat_completions(i + 1, message))
    
    # asyncio.gather
    input_messages = {}
    for i, user_input in enumerate(messages):
        message = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        input_messages[i] = message
    await asyncio.gather(*[get_chat_completions(i + 1, input_message) for i, input_message in input_messages.items()])
    
            
if __name__ == "__main__":
    system_prompt = "You are a helpful coding assistant. Please answer in Chinese."
    inputs = [
        "请用一句话解释什么是递归？",
        "请用一句话解释什么是闭包？",
        "请用一句话解释什么是装饰器？",
        "请用一句话解释什么是生成器？",
        "请用一句话解释什么是协程？"
    ]
    
    print(f"sync started at {time.strftime('%X')}")
    sync_get_chat_completions(system_prompt, inputs)
    print(f"sync finished at {time.strftime('%X')}")
    print(f"async started at {time.strftime('%X')}")
    asyncio.run(async_get_chat_completions(system_prompt, inputs))
    print(f"async finished at {time.strftime('%X')}")
    
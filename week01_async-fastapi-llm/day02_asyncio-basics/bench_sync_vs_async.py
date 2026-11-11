from openai import OpenAI, AsyncOpenAI
import os
from pathlib import Path
from dotenv import load_dotenv
import time
import asyncio

load_dotenv(Path(__file__).parent.parent.parent / ".env")

async_client = AsyncOpenAI(base_url=os.environ["API_BASE_URL"], api_key=os.environ["OPENAI_API_KEY"])
sync_client = OpenAI(base_url=os.environ["API_BASE_URL"], api_key=os.environ["OPENAI_API_KEY"])
GEMINI_MODEL = "gemini-3.8-flash-high"

async def get_responses(i, input_list):
    response = await async_client.responses.create(
        model=GEMINI_MODEL,
        input=input_list
    )
    # print(f"Response: {i}, {response.output_text}")
    
async def async_get_responses(system_prompt, inputs):    
    # Use asyncio.TaskGroup to run multiple tasks concurrently
    async with asyncio.TaskGroup() as tg:
        for i, user_input in enumerate(inputs):
            input_list = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
            tg.create_task(get_responses(i + 1, input_list))
    
    # Alternatively, you can use asyncio.gather to run multiple tasks concurrently
    # input_lists = {}
    # for i, user_input in enumerate(inputs):
    #     input_list = [
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": user_input}
    #     ]
    #     input_lists[i] = input_list
    # await asyncio.gather(*[get_responses(i + 1, input_list) for i, input_list in input_lists.items()])


def sync_get_responses(system_prompt, inputs):
    for i, user_input in enumerate(inputs):
        input_list = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        response = sync_client.responses.create(
            model=GEMINI_MODEL,
            input=input_list
        )
        # print(f"Response: {i + 1}, {response.output_text}")
    
if __name__ == "__main__":
    system_prompt = "You are a helpful coding assistant. Please answer in Chinese."
    inputs = [
        "请用一句话解释什么是递归？",
        "请用一句话解释什么是闭包？",
        "请用一句话解释什么是装饰器？",
        "请用一句话解释什么是生成器？",
        "请用一句话解释什么是协程？"
    ]
    
    # print(f"async started at {time.strftime('%X')}")
    # asyncio.run(async_get_responses(system_prompt, inputs))
    # print(f"async finished at {time.strftime('%X')}")
    # print(f"sync started at {time.strftime('%X')}")
    # sync_get_responses(system_prompt, inputs)
    # print(f"sync finished at {time.strftime('%X')}")
    
    sync_time = 0
    async_time = 0
    cycle = 3
    
    for i in range(cycle):
        t0 = time.perf_counter()
        sync_get_responses(system_prompt, inputs)
        t1 = time.perf_counter()
        sync_time += t1 - t0
        asyncio.run(async_get_responses(system_prompt, inputs))
        t2 = time.perf_counter()
        async_time += t2 - t1

    print(f"Average sync time over {cycle} cycles: {sync_time / cycle:.4f} seconds")
    print(f"Average async time over {cycle} cycles: {async_time / cycle:.4f} seconds")
from openai import OpenAI, AsyncOpenAI
import json
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent.parent / ".env")

API_BASE_URL = os.environ["API_BASE_URL"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
client = AsyncOpenAI(base_url=API_BASE_URL, api_key=OPENAI_API_KEY)
MODEL = "gpt-6.1-terra"

# 1. Define a list of callable tools for the model
tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Retrieves current weather for the given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia"
                },
            },
            "required": ["location"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]

async def get_responses(i, input_list):
    response = await client.responses.create(
        model=MODEL,
        input=input_list,
        tools=tools,
    )
    
    # Save function call outputs for subsequent requests
    input_list += response.output

    for item in response.output:
        if item.type == "function_call":
            print(item)
            exit()
            if item.name == "get_weather":
                # 3. Execute the function logic for get_weather
                location = json.loads(item.arguments)["location"]
                weather = get_weather(location)

                # 4. Provide function call results to the model
                input_list.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": weather,
                    }
                )

    response = await client.responses.create(
        model=MODEL,
        tools=tools,
        input=input_list,
    )

    # 5. The model should be able to give a response!
    print(f"{i}: {response.output_text}")

def get_weather(location):
    return f"The weather in {location} is 75 degrees"

# Create a running input list we will add to over time
async def async_get_weathers(places):
    async with asyncio.TaskGroup() as tg:
        for i, place in enumerate(places):
            input_list = [{"role": "user", "content": f"What is the weather in {place}?"}]
            tg.create_task(get_responses(i + 1, input_list))

if __name__ == "__main__":
    places = ["Beijing and Tianjin", "Shanghai", "Shenzhen", "Zhengzhou", "Chengdu", "Xian"]
    asyncio.run(async_get_weathers(places))

            
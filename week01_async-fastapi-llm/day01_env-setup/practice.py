from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

client = OpenAI(base_url=os.environ["API_BASE_URL"], api_key=os.environ["OPENAI_API_KEY"])
MODEL = "gemini-3.8-flash-high"

def get_responses(input_list):
    response_1 = client.responses.create(
        model=MODEL,
        input=input_list
    )
    print(f"Response 1: {response_1.output_text}, Usage Input: {response_1.usage.input_tokens}, Output: {response_1.usage.output_tokens}, Total: {response_1.usage.total_tokens}")
    
    input_list = input_list + [
        {"role": "assistant", "content": response_1.output_text},
        {"role": "user", "content": "基于刚才的解释，写一个用Python实现的示例。"}
    ]
    response_2 = client.responses.create(
        model=MODEL,
        input=input_list
    )
    print(
        f"Response 2: {response_2.output_text}",
        f"Usage Input: {response_2.usage.input_tokens}",
        f"Output: {response_2.usage.output_tokens}",
        f"Total: {response_2.usage.total_tokens}"
    )
    
if __name__ == "__main__":
    input_list = [
        {"role": "system", "content": "You are a brillant code engineer. Answer me with Chinese."},
        {"role": "user", "content": "用一句话解释贪心算法"}
    ]
    get_responses(input_list)
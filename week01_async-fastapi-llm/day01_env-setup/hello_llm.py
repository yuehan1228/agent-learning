from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

client = OpenAI(base_url=os.environ["API_BASE_URL"], api_key=os.environ["OPENAI_API_KEY"])
GEMINI_MODEL = "gemini-3.8-flash-high"

def get_responses(input_list):
    response_1 = client.responses.create(
        model=GEMINI_MODEL,
        input=input_list
    )
    print(f"Response 1: {response_1.output_text}, Usage: prompt: {response_1.usage.input_tokens}, completion: {response_1.usage.output_tokens}, total: {response_1.usage.total_tokens}\n")

    input_list = input_list + [
        {"role": "assistant", "content": response_1.output_text},
        {"role": "user", "content": "基于上面的解释，写一个最简单的 Python 示例。"}
    ]       

    response_2 = client.responses.create(
        model=GEMINI_MODEL,
        input=input_list
    )
    print(f"Response 2: {response_2.output_text}, Usage: prompt: {response_2.usage.input_tokens}, completion: {response_2.usage.output_tokens}, total: {response_2.usage.total_tokens}\n")
    return response_2
    
def get_chat_completions(messages):
    response_1 = client.chat.completions.create(
        model=GEMINI_MODEL,
        messages=messages
    )
    assistant_reply_1 = response_1.choices[0].message.content
    print(f"Assistant 1: {assistant_reply_1}, Usage: prompt: {response_1.usage.prompt_tokens}, completion: {response_1.usage.completion_tokens}, total: {response_1.usage.total_tokens}\n")

    messages = messages + [
        {"role": "assistant", "content": assistant_reply_1},
        {"role": "user", "content": "基于上面的解释，写一个最简单的 Python 示例。"}
    ]
    
    response_2 = client.chat.completions.create(
        model=GEMINI_MODEL,
        messages=messages
    )
    assistant_reply_2 = response_2.choices[0].message.content
    print(f"Assistant 2: {assistant_reply_2}, Usage: prompt: {response_2.usage.prompt_tokens}, completion: {response_2.usage.completion_tokens}, total: {response_2.usage.total_tokens}\n")
    return response_2
    
if __name__ == "__main__":
    input_list = [
        {"role": "system", "content": "You are a helpful coding assistant. Please answer in Chinese."},
        {"role": "user", "content": "请用一句话解释什么是递归？"}
    ]
    result = get_chat_completions(input_list)
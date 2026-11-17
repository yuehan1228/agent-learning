from openai import OpenAI, AsyncOpenAI
import json
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path
from simpleeval import simple_eval
import time

load_dotenv(Path(__file__).parent.parent.parent / ".env")

API_BASE_URL = os.environ["API_BASE_URL"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
async_client = AsyncOpenAI(base_url=API_BASE_URL, api_key=OPENAI_API_KEY)
client = OpenAI(base_url=API_BASE_URL, api_key=OPENAI_API_KEY)
MODEL = "gpt-6.1-terra"

async def get_weather(location):
    return f"The weather in {location} is 75 degrees"

async def calculator(args: dict) -> str:
    await asyncio.sleep(1)
    expression = args["expression"]
    result = simple_eval(expression)
    return str(result)

async def read_local_file(args: dict) -> str:
    await asyncio.sleep(1)
    file_path = args["file_path"]
    start_line = args.get("start_line")
    end_line = args.get("end_line")
    encoding = args.get("encoding")
    
    selected_lines = []
    
    try:
        with open(file_path, "r", encoding=encoding) as f:
            for line_num, line in enumerate(f, start=1):
                if line_num < start_line:
                    continue
                if line_num > end_line:
                    break
                
                selected_lines.append(f"{line_num}: {line.rstrip(chr(10) + chr(13))}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"文件不存在：{file_path}，请检查路径。我这是linux系统，用户名为yh,‘~’一般代表什么呢？") from e
            
    return "\n".join(selected_lines)

TOOL_REGISTRY = {
    "get_weather": {
        "func": get_weather,
        "schema": {
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
    },
    "calculator": {
        "func": calculator,
        "schema": {
            "type": "function",
            "description": "用于执行精确的数学算术运算。当用户问题涉及多位数乘除、混合运算或需要精确数值结果时调用此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "标准数学表达式，仅包含数字、括号及运算符（+、-、*、/、**、%），例如 '(3847 * 926) - 15420'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    "read_local_file": {
        "func": read_local_file,
        "schema": {
            "type": "function",
            "description": "读取本地文件系统中的纯文本文件内容（如代码文件、配置文件、Markdown、CSV 或日志）。当需要查看特定文件内容以回答问题或排查错误时调用。不要用于读取图片、音频、压缩包等二进制文件，也不要用于访问网络 URL。",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "目标文件的相对路径（推荐，相对于当前工作目录）或绝对路径，例如 'src/main.py' 或 'logs/error.log'"
                    },
                    "start_line": {
                        "type": "integer",
                        "description": "起始读取行号（从 1 开始计数），默认从第 1 行开始",
                        "minimum": 1
                    },
                    "end_line": {
                        "type": "integer",
                        "description": "结束读取行号（包含该行）。读取大文件时建议每次限制在 200 到 500 行以内，不传则默认读取至文件末尾或达到长度上限为止",
                        "minimum": 1
                    },
                    "encoding": {
                        "type": "string",
                        "enum": ["utf-8", "gbk", "ascii", "latin-1"],
                        "description": "文件字符编码格式，默认 'utf-8'"
                    }
                },
                "required": ["file_path"]
            }
        }
    }
}

tools = [
    {"name": name, **tool["schema"]} for name, tool in TOOL_REGISTRY.items()
]

async def run_call(item) -> dict:
    tool = TOOL_REGISTRY.get(item.name)
    if tool is None:
        output = f"Error: unknown tool {item.name}"
    else:
        try:
            output = await tool["func"](json.loads(item.arguments))
        except Exception as e:
            output = f"Error: {type(e).__name__}: {e}"
    return {"type": "function_call_output", "call_id": item.call_id, "output": output}

async def run_tool_loop(question: str, parallel: bool = True, max_cycles: int = 5) -> str:
    input_list = [
        {"role": "system", "content": "You are a helpful assistant and answer with chinese."},
        {"role": "user", "content": question}
    ]
    
    for i in range(max_cycles):
        response = await async_client.responses.create(model=MODEL, input=input_list, tools=tools)
        input_list += response.output  # 原样保留（含 reasoning 项）

        calls = [item for item in response.output if item.type == "function_call"]
        
        if not calls:
            return response.output_text
        
        for call in calls:
            print(f"[第 {i + 1} 轮调用]: {call.name} arguments={call.arguments}")

        t0 = time.perf_counter()
        if parallel:
            outputs = await asyncio.gather(*(run_call(c) for c in calls))
        else:
            outputs = [await run_call(c) for c in calls]
        t1 = time.perf_counter()
        
        for output in outputs:
            print(f"[第 {i + 1} 轮结果]: {output}, 耗时：{t1 - t0:.2f}")
        input_list += outputs

    raise RuntimeError("达到最大请求轮数，模型仍在调用工具")
    

async def main():
    # question = "计算一下 ((3847 * 926) - 15420) + 5418，然后读取 /home/yh/rz.txt 文件并展示第10行到第50行的内容"
    question = (
        "这是工具错误恢复实验。"
        "1. 请计算 2 的 10 次方，必须使用 calculator。"
        "第一次调用请故意把 expression 原样设为 '2^10'，以触发参数错误。"
        "收到工具错误后，请根据错误提示修正表达式并再次调用 calculator，"
        "成功后再回答最终结果，不要只口头解释应该如何修改。"
        "2. 读取本地文件，必须使用 read_local_file。"
        "第一此调用请故意把 file_path 设为 ~/rz.txt，以触发读取文件失败。"
        "收到工具错误后，根据错误提示修正文件路径并再次调用 read_local_file，"
        "成功后再回答最终结果，不要只口头解释应如何修改。"
    )
    print(await run_tool_loop(question))

if __name__ == "__main__":
    asyncio.run(main())
            
"""并行工具调用演示：一次响应里模型发起多个 function_call，本地用 asyncio.gather 并发执行。"""
import asyncio
import json
import time

from tool_demo_1 import MODEL, client, tools


async def get_weather(location: str) -> str:
    await asyncio.sleep(1)  # 模拟慢工具（如网络请求），用来体现并发收益
    return f"The weather in {location} is 75 degrees"


TOOL_REGISTRY = {"get_weather": get_weather}


async def run_call(item) -> dict:
    """执行单个 function_call，返回对应的 function_call_output；任何错误都当作结果回传给模型。"""
    func = TOOL_REGISTRY.get(item.name)
    if func is None:
        output = f"Error: unknown tool {item.name}"
    else:
        try:
            output = await func(**json.loads(item.arguments))
        except Exception as e:
            output = f"Error: {type(e).__name__}: {e}"
    return {"type": "function_call_output", "call_id": item.call_id, "output": output}


async def run_tool_loop(question: str, parallel: bool = True) -> str:
    input_list = [{"role": "user", "content": question}]
    response = await client.responses.create(model=MODEL, input=input_list, tools=tools)
    input_list += response.output  # 原样保留（含 reasoning 项）

    calls = [item for item in response.output if item.type == "function_call"]
    print(f"模型一次返回了 {len(calls)} 个 function_call: {[c.arguments for c in calls]}")

    t0 = time.perf_counter()
    if parallel:
        outputs = await asyncio.gather(*(run_call(c) for c in calls))
    else:
        outputs = [await run_call(c) for c in calls]
    print(f"{'并发' if parallel else '串行'}执行 {len(calls)} 个工具耗时: {time.perf_counter() - t0:.2f}s")
    input_list += outputs

    response = await client.responses.create(model=MODEL, input=input_list, tools=tools)
    return response.output_text


async def main():
    question = "请分别告诉我北京、上海、深圳、成都的天气。"
    for parallel in (False, True):
        print(f"\n=== parallel={parallel} ===")
        print(await run_tool_loop(question, parallel))


if __name__ == "__main__":
    asyncio.run(main())

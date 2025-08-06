from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, set_tracing_disabled,enable_verbose_stdout_logging, function_tool, AgentOutputSchemaBase
from dotenv import load_dotenv
import os
from rich import print
import asyncio

set_tracing_disabled(disabled=True)
load_dotenv()

enable_verbose_stdout_logging()

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

@function_tool
def sum_tool(a:int,b:int,) -> str:
    """ Args:
        a(int): first operand
        b(int): second operand

    Returns:
       The sum of a and b.
    
    """
    return f"{a + b}"


sum_agent = Agent(
    name="Sum Agent",
    instructions="Sum two numbers",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client),
)

agent = Agent(
    name="helper",
    instructions="You are a helper",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client),
    # tools=[sum_tool],
    handoffs=[sum_agent]
)
print(f"{'-' * 40} NEW AGENT {'-' * 40}")

async def main():
    result = await Runner.run(starting_agent=agent, input="2 + 2")
    print("result.final_output:",result)

asyncio.run(main())
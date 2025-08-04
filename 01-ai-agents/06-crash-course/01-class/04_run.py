from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner,enable_verbose_stdout_logging, set_tracing_disabled
from dotenv import load_dotenv
import os
from rich import print
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
set_tracing_disabled(disabled=True)
load_dotenv()

enable_verbose_stdout_logging()

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

# OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client),
)

async def main():
    result = await Runner.run(starting_agent=agent, input="Write an essay on allama iqbal the poet")
    print("RESULT")
    print(result)
    print("DIR(RESULT)")
    print(dir(result))

asyncio.run(main())
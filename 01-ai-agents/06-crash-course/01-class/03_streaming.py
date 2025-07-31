from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner,enable_verbose_stdout_logging
from dotenv import load_dotenv
import os
from rich import print
import asyncio

# set_tracing_disabled(disabled=True)
load_dotenv()

enable_verbose_stdout_logging()

external_client = AsyncOpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model="gemini-1.0-flash", openai_client=external_client),
)

async def main():
    result = await Runner.run(starting_agent=agent, input="Write a letter to elder bro")

    async for event in result.stream_events():
        print("EVENT")
        print(event)

asyncio.run(main())
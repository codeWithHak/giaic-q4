from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
set_tracing_disabled(disabled=True)


API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=external_client)
)

async def main():
    result = await Runner.run(starting_agent=agent, input="Hello")
    print(result.final_output)
    
asyncio.run(main())



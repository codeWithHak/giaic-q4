from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI, Runner, set_tracing_disabled 
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

set_tracing_disabled(disabled=True)

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
model= os.getenv('MODEL')

client = AsyncOpenAI(
    api_key = api_key,
    base_url = base_url
)

async def main():
    agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model=model, openai_client=client)
)

    user_input = input("Ask me anything: ")

    result = await Runner.run(
        agent,
        user_input
    )
    
    return result.final_output

print(asyncio.run(main()))
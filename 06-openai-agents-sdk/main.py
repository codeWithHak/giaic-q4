import asyncio
from openai import AsyncOpenAI # chat completions
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
import os
from dotenv import load_dotenv
load_dotenv()
set_tracing_disabled(disabled=True) # Open AI Tracing == Disable
print("set tracing passed")

client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

print("client set")


async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="LahoreTA",
        instructions="You only respond in english.",
        model=OpenAIChatCompletionsModel(model=os.getenv("MODEL"), openai_client=client),
    )

    result = await Runner.run(
        agent, # starting agent
        "What is your name?.", # request
    )
    print("before printing result")
    print(result.final_output)


asyncio.run(main())
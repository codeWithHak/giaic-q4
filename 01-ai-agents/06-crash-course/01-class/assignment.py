# Implement Delayd Tool Calling And Handle It With Fallbacks, (e.g: Delayed API Calls)

from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner,enable_verbose_stdout_logging, set_tracing_disabled, function_tool, AgentOutputSchemaBase 
from dotenv import load_dotenv
import os
from rich import print
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents.result import RunResultStreaming
import time

load_dotenv()

enable_verbose_stdout_logging()



async def get_weather_data(city:str) -> str:
    print("\nGOING TO SLEEP\n")
    await asyncio.sleep(30)
    print("\nAwake\n")
    return f"Weather in {city} is sunny"


async def safe_function(city:str) -> str:
    """Fetch weather with a 10s timeout—return a fallback if slow."""   

    try:
        return await asyncio.wait_for(get_weather_data(city), timeout=20.0)
    
    except asyncio.TimeoutError:
        return "TOOL IS SLOW"

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

# OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client),
    tools=[function_tool(func=safe_function ,name_override='fetch_weather')]
)

async def main():
    result = Runner.run_streamed(starting_agent=agent, input="What's the weather in karachi")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta)
    

asyncio.run(main())
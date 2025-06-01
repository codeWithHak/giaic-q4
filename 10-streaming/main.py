from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, RunConfig
from openai.types.responses import ResponseTextDeltaEvent
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

external_client = AsyncOpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

model = OpenAIChatCompletionsModel(
    model=os.getenv('MODEL'),
    openai_client=external_client
)

run_config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


async def main():
    agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant that only replies in roman urdu"
)

    result = Runner.run_streamed(
        agent,
        "hello, create an essay on a rainy day, rainy day means a bad day",
        run_config=run_config
    )
    
    async for event in result.stream_events():
        if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
        
asyncio.run(main())

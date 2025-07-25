from agents import Agent, Runner, enable_verbose_stdout_logging, set_default_openai_api
from openai.types.responses import ResponseTextDeltaEvent
import asyncio
from dotenv import load_dotenv

set_default_openai_api("chat_completions")

load_dotenv()
enable_verbose_stdout_logging()

async def main():


    agent = Agent(
        name="Assistant",
        instructions="you're a helpful assistant"
    )

    result = Runner.run_streamed(
        starting_agent=agent,
        input="Write an essay on a rainy day",
        )
    
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="" ,flush=True)

if __name__ == "__main__":
    asyncio.run(main())


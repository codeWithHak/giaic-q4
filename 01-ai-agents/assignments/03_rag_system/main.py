from agents import Agent, Runner
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_DB_ID = os.getenv("VECTOR_DB_ID")

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You're a helpful assistant"
    )

    result = await Runner.run(starting_agent=agent, input="Hello")
    
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())
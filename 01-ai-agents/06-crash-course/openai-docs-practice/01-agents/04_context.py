from agents import Agent, Runner, enable_verbose_stdout_logging, RunContextWrapper,function_tool, set_default_openai_api
import asyncio
from dataclasses import dataclass
from dotenv import load_dotenv

set_default_openai_api("chat_completions")

load_dotenv()

@dataclass
class UserInfo:
    name: str
    age: int


@function_tool
async def fetch_user_profession(wrapper:RunContextWrapper[UserInfo]) -> str:
    """Fetch the  profession of the user . Call this function to get user's profession""" 
    return f"The profession of {wrapper.context} is Agentic AI Developer"


async def main():
    
    user_info = UserInfo(name="Huzair Ahmed Khan", age=10)

    agent = Agent[UserInfo](
        name="You're a helpful assistant",
        instructions="You will get the user details as requested",
        tools=[fetch_user_profession])

    result = await Runner.run(
        starting_agent=agent,
        input="What is the profession of the user",
        context=user_info
        )
    
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())


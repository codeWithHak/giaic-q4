#type:ignore
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, RunContextWrapper
from dotenv import load_dotenv
import os
from dataclasses import dataclass
import asyncio

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY=os.getenv("API_KEY")
BASE_URL=os.getenv("BASE_URL")

client = AsyncOpenAI(
    api_key = API_KEY,
    base_url= BASE_URL
)

# using data class here we can use simple calss as well but dataclass is more efficient 
@dataclass
class UserInfo:
    name:str
    age:int


@function_tool
async def fetch_user_details(wrapper:RunContextWrapper[UserInfo]) -> str:
    """Returns user name and age"""
    return f"Name:{wrapper.context.name}, Age:{wrapper.context.age}"

user_info = UserInfo(name="Huzair", age=19)

agent = Agent[UserInfo](
    name="Assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model='gemini-2.0-flash', openai_client=client),
    tools=[fetch_user_details]
)




user_input = input("Ask me anything: ")

result = Runner.run_sync(starting_agent=agent, input=user_input, context=user_info)
print(result.final_output)
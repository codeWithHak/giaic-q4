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

@dataclass
class UserInfo:
    name:str
    age:int
    email:str

@function_tool
async def fetch_user_details(wrapper:RunContextWrapper[UserInfo]):
    """Returns user name, age and email"""
    # if we dont return the email but have email in user info what happens?
    # agent loop will still call this (fetch_user_details) tool, it will see there's only name and age return not email
    # so it will not get the email from agent and hence ll won't get mail so it will not give output of what's email of user!
    return wrapper.context.name, wrapper.context.age, 

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client),
    tools=[fetch_user_details]
)

user_info = UserInfo(name="Huzair",age=19, email="huzairahmedkhan@gmail.com")

async def main():
    result = await Runner.run(starting_agent=agent, input="What's the email of user", context=user_info)
    print(result.final_output)
    
asyncio.run(main())
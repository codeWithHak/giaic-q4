from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunContextWrapper
from dotenv import load_dotenv
import os
from pydantic import BaseModel
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
class UserContext:
    name:str
    age:int

def dynamic_instructions(context:RunContextWrapper[UserContext], agent:Agent[UserContext]) -> str :
    return f"The username is {context.context.name}, greet them first. And then help them with their querry"
    
context = UserContext(name="huzair", age=19)
agent = Agent(
    name="Tournament Marketing Agent",
    instructions=dynamic_instructions,
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client),
    
)

async def main():
    result = await Runner.run(starting_agent=agent, input="How many types of datatypes are there in python?", context=context)
    print(result.final_output)
    
asyncio.run(main())
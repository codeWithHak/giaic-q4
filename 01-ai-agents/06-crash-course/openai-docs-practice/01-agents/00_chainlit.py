from agents import Agent, Runner, set_default_openai_api
from dotenv import load_dotenv
import os
import chainlit as cl

set_default_openai_api("chat_completions")

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model="gpt-4o",

)



# @cl.on_chat_start
# async def handle_chat_start():
#     response = await cl.Message(content="Hello, Welcome to Huzair GPT!").send()
#     return response

@cl.on_message
async def handle_message(message:cl.Message):
    result = Runner.run_sync(starting_agent=agent, input=message.content)
    response = await cl.Message(content=f"{result.final_output}").send()
    return response
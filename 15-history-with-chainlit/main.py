#type:ignore

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
import os
import chainlit as cl
# import asyncio
 
load_dotenv()
set_tracing_disabled(disabled=True)
 
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")
 
external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model= OpenAIChatCompletionsModel(model=MODEL, openai_client=external_client)
)

@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set(key="empty_history", value=[])
    await cl.Message(content="Hello, How may I help you today!").send()
    
@cl.on_message
async def handle_message(message):
    history = cl.user_session.get("empty_history")
    history.append({"role":"user", "content":message.content})
    
    result = await Runner.run(starting_agent=agent, input=history)
    
    history.append({"role":"assistant", "content":result.final_output})
    cl.user_session.set("empty_history",history)

    message = cl.Message(content=result.final_output)
    await message.send()




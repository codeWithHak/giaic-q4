#type:ignore
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from openai.types.responses import ResponseTextDeltaEvent
import os
from dotenv import load_dotenv
import asyncio
import chainlit as cl

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
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=external_client)
)
    
@cl.on_chat_start
async def handle_chat_start():
    await cl.Message(content="Hello, How may I help you?").send()
    
    
@cl.on_message
async def handle_message(message):
    response_text = cl.Message(content=" ")
    await response_text.send()
    
    result = Runner.run_streamed(starting_agent=agent, input=message.content)
    
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            await response_text.stream_token(event.data.delta)

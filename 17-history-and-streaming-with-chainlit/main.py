#type:ignore
from agents import AsyncOpenAI, Runner, OpenAIChatCompletionsModel, Agent, set_tracing_disabled
from dotenv import load_dotenv
import os
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
    name="Helpful Assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=external_client)
)



@cl.on_message
async def res(message):
    result = await Runner.run(agent,message.content)
    message = cl.Message(content=f"{result.final_output}")
    await message.send()


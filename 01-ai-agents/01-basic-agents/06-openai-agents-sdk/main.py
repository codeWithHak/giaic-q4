import asyncio
from openai import AsyncOpenAI # chat completions
from agents import Agent, OpenAIChatCompletionsModel, Runner
import os
from dotenv import load_dotenv
import chainlit as cl

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("BASE_URL")
url = os.getenv("URL")
model = os.getenv("MODEL")



print("set tracing passed")

client = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
)

print("client set")


    # This agent will use the custom LLM provider
agent = Agent(
    name="Assistant",
    instructions="You only respond in english.",
    model=OpenAIChatCompletionsModel(model=model, openai_client=client),
)

print("before printing result")


@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history",[])
    await cl.Message(content="Hello how may I help you sirrr").send()

@cl.on_message
async def handle_message(message:cl.Message):
    
    history = cl.user_session.get("history")
    
    history.append({"role":"user", "content":message.content})
    result = await Runner.run(
        agent, # starting agent
        input=history
)   
    history.append({"role":"assistant", "content":result.final_output})
    cl.user_session.set("history",history)
    
    await cl.Message(content=result.final_output).send() 

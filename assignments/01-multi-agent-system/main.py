from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI, Runner, set_tracing_disabled
from dotenv import load_dotenv
import os
import asyncio
# from openai import AsyncOpenAI

load_dotenv()
set_tracing_disabled(disabled=True)
external_client = AsyncOpenAI(
    api_key = os.getenv("API_KEY"),
    base_url = os.getenv("BASE_URL")
)

model = OpenAIChatCompletionsModel( model="gemini-2.0-flash", openai_client=external_client)

researcher = Agent(
    name="Expert LinkedIn Researcher Agent",
    instructions="You are an expert researcher who research and find topics for users to write posts for their LinkedIn",
    model=model,
    handoff_description = "Handoff to researcher if task is related to research or finding topics to post on LinkedIn"
)

writer = Agent(
    name="Expert LinkedIn Post Writer Agent",
    instructions="You are an expert writer who writes LinkedIn posts for users",
    model=model,
    handoff_description = "Handoff to writer agent if the task is about writing a post"   
)

hook_writer = Agent(
    name="Expert LinkedIn hook writer",
    instructions="You are an Expert LinkedIn hook writer, who writes catchy hooks based on the post content, that grabs instant attention",
    model=model,
    handoff_description="Handoff to hook_writer if task is about writing hooks"
)

async def agent(user_input):
    triage_agent = Agent(
        name="Triage Agent",
        instructions = "You will take input from the users and delegate tasks to specific agents based on the user input!",
        model=model,
        handoffs=[researcher,writer,hook_writer]
    )
    
    result = await Runner.run(agent,user_input)
    print(result.final_output)
    
async def main():    
    user_input = input("Ask me anything: ")
    await agent(user_input)
if __name__ == "__main__":
    asyncio.run(main())
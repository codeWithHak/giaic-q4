from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI, Runner, set_tracing_disabled
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples. Start the output with Math agent running...",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly. Start the output with History agent running...",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="You will decide which agent to use based on user's homework question, if you decide to use math agent you must give the output starting with: Math agent running..., if you decide to use History agent you must give the output starting with: History agent running...",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client),
    handoffs=[math_tutor_agent,history_tutor_agent]
)


async def main():
    result = await Runner.run(starting_agent=triage_agent, input="Explain lcm")
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())
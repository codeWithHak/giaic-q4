from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

set_tracing_disabled(disabled=True)
load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

client = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
)

agent = Agent(
    name="Assistant",
    instructions="You're a helpful assistant",
    model=OpenAIChatCompletionsModel(model='gemini-2.0-flash',openai_client=client)
)

user_input = input("Ask me anything: ")

result = Runner.run_sync(
    agent,
    user_input
)

print(result.final_output)
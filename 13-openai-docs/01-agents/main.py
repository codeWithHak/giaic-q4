from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
import os

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY=os.getenv("API_KEY")
BASE_URL=os.getenv("BASE_URL")


client = AsyncOpenAI(
    api_key = API_KEY,
    base_url= BASE_URL
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model='gemini-2.0-flash', openai_client=client)
)

result = Runner.run_sync(agent,"Write an essay on 'A Rainy Day'")

print(result.final_output)
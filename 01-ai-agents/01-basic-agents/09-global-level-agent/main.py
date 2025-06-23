from agents import Agent,AsyncOpenAI,Runner, set_default_openai_api, set_default_openai_client, set_tracing_disabled
import os
from dotenv import load_dotenv

load_dotenv()

set_tracing_disabled(disabled=True)

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

set_default_openai_api('chat_completions')

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

set_default_openai_client(external_client)

agent = Agent(
    name="Assitant",
    instructions="You are a helpful assistant tha only replies in roman urdu",
    model=MODEL
)

result = Runner.run_sync(agent,"Hello")
print(result.final_output)


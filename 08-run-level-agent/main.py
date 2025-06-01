from agents import Agent, Runner, RunConfig, OpenAIChatCompletionsModel, AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

run_config = RunConfig(
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=external_client),
    model_provider=external_client,
    tracing_disabled=True   
)

agent=Agent(
    name="Assitant",
    instructions="You are a helpful assistant that replies only in roman urdu."
)
user_input = input("Ask me anything: ")

result = Runner.run_sync(
    agent,
    user_input,
    run_config=run_config
)


print(result.final_output)
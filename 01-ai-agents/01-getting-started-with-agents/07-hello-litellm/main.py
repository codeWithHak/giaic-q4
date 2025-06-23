from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel 
import os
from dotenv import load_dotenv

load_dotenv()

## set ENV variables
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")

agent = Agent(
    name="Assitant",
    instructions='You are a helpful assistant that inly reply in roman urdu.',
    model=LitellmModel(model=MODEL, api_key=API_KEY)
)

user_input=input("Ask me anything: ")

result = Runner.run_sync(
    agent,
    user_input
)

print(result.final_output)
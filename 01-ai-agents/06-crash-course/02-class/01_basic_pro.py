from agents import Agent, Runner,enable_verbose_stdout_logging
from dotenv import load_dotenv
import os
from rich import print

load_dotenv()

enable_verbose_stdout_logging()

agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant",
    model="gpt-4o-mini"
)

result = Runner.run_sync(starting_agent=agent, input="What is ai")

print("result:",result.final_output)
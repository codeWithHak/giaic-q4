from agents import Agent, Runner, enable_verbose_stdout_logging, set_default_openai_api
from dotenv import load_dotenv
import os

enable_verbose_stdout_logging()
set_default_openai_api("chat_completions")

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model="gpt-4o",

)

result = Runner.run_sync(starting_agent=agent, input="Hello which llm e.g(gemini) and model e.g(gemini-2.5-flash) is this")
print(result.final_output)
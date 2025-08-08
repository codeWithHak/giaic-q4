from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, set_tracing_disabled,enable_verbose_stdout_logging
from dotenv import load_dotenv
import os
from rich import print

set_tracing_disabled(disabled=True)
load_dotenv()



enable_verbose_stdout_logging()

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("BASE_URL")
) 

agent = Agent(
    name="Poet",
    instructions="You are a poet, reply to queries in haiku",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)
)

cloned_agent = agent.clone(
    name="Software Engineer",
    instructions="You are a software engineer, reply in technical terms."
)

result = Runner.run_sync(starting_agent=cloned_agent, input="What is ai")

print("result:",result.final_output)
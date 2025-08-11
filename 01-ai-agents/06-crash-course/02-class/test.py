from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, set_tracing_disabled,enable_verbose_stdout_logging, WebSearchTool
from dotenv import load_dotenv
import os
from rich import print

load_dotenv()



enable_verbose_stdout_logging()


agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant",
    model='gpt-4o-mini',
    tools=[WebSearchTool()]
    )

result = Runner.run_sync(starting_agent=agent, input="Current ai trends")

print("result:",result.final_output)
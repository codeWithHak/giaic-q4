from agents import Agent, Runner,enable_verbose_stdout_logging, RunHooks
from dotenv import load_dotenv
from rich import print

load_dotenv()

enable_verbose_stdout_logging()

agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant",
    model="gpt-4o-mini"
)

class TestRunHooks(RunHooks):
    async def on_agent_start(self,context,agent):
        print(f "\n[ON_AGENT_START]")



result = Runner.run_sync(starting_agent=agent, input="What is ai", hooks=TestRunHooks())

print("result:",result.final_output)
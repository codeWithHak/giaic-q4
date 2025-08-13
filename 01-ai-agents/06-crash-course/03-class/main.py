from agents import Agent, Runner,enable_verbose_stdout_logging, trace
from agents.tracing import util
from dotenv import load_dotenv
from rich import print

load_dotenv()

enable_verbose_stdout_logging()

agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant",
    model="gpt-4o-mini"
)

trace_id=util.gen_trace_id()
print(trace_id)

my_trace = trace(workflow_name="Mera Naya Shana Agent Workflow", trace_id=trace_id)
my_trace.start()

result = Runner.run_sync(starting_agent=agent, input="What is ai")

print("result:",result.final_output)
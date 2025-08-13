from agents import Agent, Runner,enable_verbose_stdout_logging, handoff, function_tool
from agents.extensions import handoff_filters
from dotenv import load_dotenv
from rich import print

load_dotenv()

enable_verbose_stdout_logging()

@function_tool
def fetch_weather(city:str) -> str:
    return f"weather in {city} is sunny"


sales_inquiry_agent = Agent(
    name="Inquiry Agent",
    instructions="You are responsible for managing all user inquiries according to sales.",
    model="gpt-4o-mini",
)

general_agent = Agent(
    name="General Agent",
    instructions="You are a helpful assistant",
    model="gpt-4o-mini",
    tools=[fetch_weather],
    handoffs=[handoff(
        agent=sales_inquiry_agent,
        input_filter=handoff_filters.remove_all_tools
        )]
)

 


result = Runner.run_sync(starting_agent=general_agent, input="What's the weather in Karachi and why sales team is not responding?")

print("result:",result.final_output)
print("result:",result.last_agent.name)
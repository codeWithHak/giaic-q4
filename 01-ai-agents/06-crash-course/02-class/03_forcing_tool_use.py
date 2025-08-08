from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, set_tracing_disabled,enable_verbose_stdout_logging, function_tool
from agents.agent import StopAtTools
from dotenv import load_dotenv
import os
from rich import print

print(f"{'-' * 20} New Agent {'-' * 80}")

set_tracing_disabled(disabled=True)
load_dotenv()

enable_verbose_stdout_logging()

@function_tool
def get_weather(city:str) -> str:
    return f"The weather in {city} is suiiiiny."

# @function_tool
# def get_info(city:str) -> str:
#     return f"The info is that {city} is in danger"

# @function_tool
# def famous_dish(city:str) -> str:
#     return f"Biryani is famous in {city} "

# @function_tool
# def country_capital(country:str) -> str:
#     return f"The capital of {country} is Karachi"

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("BASE_URL")
) 

agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=external_client),
    # tools=[get_weather,get_info,famous_dish, country_capital],
    tools=[get_weather],
)

result = Runner.run_sync(starting_agent=agent, input="What's the weather in karachi and provide some info about karachi. And what is the most famous dish in Karachi. And what is the capital of Pakistan.")

print("result:",result.final_output)
from agents import Agent, Runner, enable_verbose_stdout_logging, set_default_openai_api, function_tool
from dotenv import load_dotenv
import os
import requests


enable_verbose_stdout_logging()
set_default_openai_api("chat_completions")

load_dotenv()


@function_tool()
def get_weather(city:str) -> str:
    
    """Takes city as an argument
    
    Args(str):city
  
    returns weather of that city  
    """
    response = requests.get("")
    
    "Read Docs: https://www.weatherapi.com/docs/"
    "WEATHER_API_KEY=a2dc1d4874ab437189543444251707"
        
    return f"The weather in {city} is sunny"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model="gpt-4o",
    tools=[get_weather]
)

result = Runner.run_sync(starting_agent=agent, input="What's the weather in Karachi")
print(result.final_output)
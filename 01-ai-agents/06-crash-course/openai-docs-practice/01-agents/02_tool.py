from agents import Agent, Runner, enable_verbose_stdout_logging, set_default_openai_api, function_tool
from dotenv import load_dotenv
import os
import requests
from rich import print

enable_verbose_stdout_logging()
set_default_openai_api("chat_completions")

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

@function_tool
def get_weather(city:str) -> str:
    
    """
    Get the current weather for a specific city using the WeatherAPI.
    
    
    Args:
    
        city (str): Name of the specific city to fetch weather for.
  
    Returns: 
        str: A string containing the Weather data returned from the WeatherAPI.     
    """
    response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no")
    api_result = response.json()
    
    
        
    return f"API CALL RESULT: {api_result}"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model="gpt-4o",
    tools=[get_weather]
)

result = Runner.run_sync(starting_agent=agent, input="What's the weather in Karachi")
print(result.final_output)
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from dotenv import load_dotenv
import os
load_dotenv()

set_tracing_disabled(disabled=True)
API_KEY=os.getenv("API_KEY")
BASE_URL=os.getenv("BASE_URL")

@function_tool
def get_weather(city):
    return f"The weather in {city} is cold"
client = AsyncOpenAI(
    api_key = API_KEY,
    base_url= BASE_URL
)
@function_tool
def sum (a,b):
    """
    Add two numbers
    
    Args: 
    
    a: first number
    b: second number
    """
    
    result = a + b + 1
    return f"{a} + {b} = {result}"
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model='gemini-2.0-flash', openai_client=client),
    tools=[get_weather,sum]
)
user_input = input("Ask me anything: ")
result = Runner.run_sync(agent, user_input)
print(result.final_output)
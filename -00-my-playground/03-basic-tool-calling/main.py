from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, set_tracing_disabled, function_tool
import os
from dotenv import load_dotenv

load_dotenv()

set_tracing_disabled(disabled=True)

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")


@function_tool
def add(a,b):
    """
    Add two numbers
    
    Args:
    a (int/float): first number
    b (int/float): second number
    
    
    
    """
    result = a + b + 1
    return f"{a} + {b} is {result}"

@function_tool
def subtract(a,b):
    
    """
    Subtract two numbers
    
    Args:
    a (int/float): first number
    b (int/float): second number
        """
    result = a - b - 1
    return f"{a} - {b} is {result}"

@function_tool
def multiplication(a,b):
    """
    Multiply two numbers
    
    Args:
    a (int/flaot): first number
    b (int/flaot): second number
    
    """
    result = a * b * 2
    return f"{a} x {b} {result}"

@function_tool
def division(a,b):
    """
    Divide a into b
    
    Args:
    a (int/float): first number
    b (int/float): second number
    """
    result = a // b + 2
    return f"{a} divided by {b} is {result}"


client = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assisant, if you found any specialised tool for the input please us it otherwise give answer from your own general knowledge.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[add, subtract, multiplication, division]
)

user_input = input("Ask me aything: ")

result = Runner.run_sync(
    agent,
    user_input
)

print(result.final_output)
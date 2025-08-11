from agents import Agent, Runner,enable_verbose_stdout_logging, function_tool
from dotenv import load_dotenv
import os
from rich import print

load_dotenv()

enable_verbose_stdout_logging()

@function_tool
def get_weather(city:str) -> str:
    return f"The weather in {city} is sunny"


@function_tool
def translation_tool(word:str, transleted_word:str) -> str:
    return f"{word} in spanish is called {transleted_word}"

translater_agent = Agent(
    name="Translator",
    instructions="You are an expert translator",
    model="gpt-4o-mini",
    tools=[translation_tool]
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model="gpt-4o-mini",
    tools=[get_weather],
    handoffs=[translater_agent]
)

result = Runner.run_sync(starting_agent=agent, input="What's the weather like in london these days, and what we say to monday in spanish language")

print("result:",result.final_output)
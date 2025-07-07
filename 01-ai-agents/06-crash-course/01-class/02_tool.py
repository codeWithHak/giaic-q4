from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, function_tool,enable_verbose_stdout_logging
from dotenv import load_dotenv
import os
from rich import print

# set_tracing_disabled(disabled=True)
load_dotenv()

enable_verbose_stdout_logging()

@function_tool
def get_weather(city:str) -> str:
    return f"Weather in {city} is 22C"

external_client = AsyncOpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client),
    tools=[get_weather]
)

result = Runner.run_sync(starting_agent=agent, input="What's the weather in karachi")
# print(result.raw_responses[0].output[0].content[0].text)
# print(result.raw_item.content[0].text)
# print("result:",result)
print(result.final_output)
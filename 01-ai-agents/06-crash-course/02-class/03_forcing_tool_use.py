from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, set_tracing_disabled,enable_verbose_stdout_logging, function_tool, ModelSettings
from agents.agent import StopAtTools
from dotenv import load_dotenv
import os
from rich import print

print(f"{'-' * 20} New Agent {'-' * 80}")

set_tracing_disabled(disabled=True)
load_dotenv()

enable_verbose_stdout_logging()

@function_tool
def get_karachi_info(city:str) -> str:
    return f"{city} Khatrey me he bawaa"


external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("BASE_URL")
) 

agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client),
    # tools=[get_weather,get_info,famous_dish, country_capital],
    tools=[get_karachi_info],
    model_settings=ModelSettings(tool_choice="auto")
)

result = Runner.run_sync(starting_agent=agent, input="Provide some info about astronauts.")

print("result:",result.final_output)
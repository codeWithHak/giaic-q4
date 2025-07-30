from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, set_tracing_disabled,enable_verbose_stdout_logging
from dotenv import load_dotenv
import os
from rich import print

set_tracing_disabled(disabled=True)
load_dotenv()

enable_verbose_stdout_logging()

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)
)
print(f"{'-' * 40} NEW AGENT {'-' * 40}")
result = Runner.run_sync(starting_agent=agent, input="Test prompt")
# print(result.raw_responses[0].output[0].content[0].text)
# print(result.raw_item.content[0].text)
# print("result:",result)
print("result:",result)

# print("result.new_items:",result.new_items[0].agent.instructions)

# print("result.input:",result.input)
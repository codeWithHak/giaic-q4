from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()
set_tracing_disabled(disabled=True)
API_KEY=os.getenv("API_KEY")
BASE_URL=os.getenv("BASE_URL")

client = AsyncOpenAI(
    api_key = API_KEY,
    base_url= BASE_URL
)


# using data class here we can use simple calss as well but dataclass is more efficient 
@dataclass
class UserContext:
    username="Huzair Ahmed Khan"
    user_profession="Full Stack Developer"
    user_age=19

agent = Agent[UserContext](
    name="Assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model='gemini-2.0-flash', openai_client=client),
)



user_input = input("Ask me anything: ")

result = Runner.run_sync(agent, user_input)
print(result.final_output)
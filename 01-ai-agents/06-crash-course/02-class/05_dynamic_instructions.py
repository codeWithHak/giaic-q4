from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, set_tracing_disabled,enable_verbose_stdout_logging, RunContextWrapper
from dotenv import load_dotenv
import os
from rich import print
from dataclasses import dataclass

set_tracing_disabled(disabled=True)
load_dotenv()


enable_verbose_stdout_logging()


@dataclass
class User:
    name:str


def get_dynamic_prompt(ctx:RunContextWrapper[User], agent:Agent[User]) -> str:
    print("\n[CTX]",ctx)
    print("\n[AGENT]",agent)
    return f"You are an amazing and friendly assistant and your name is {ctx.context.name} that helps user in their quries in a friendly way!"

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("BASE_URL")
) 

agent = Agent(
    name="assistant",
    instructions=get_dynamic_prompt,
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)
    
)

user_info = User(name="Shapatar Assistant")

result = Runner.run_sync(starting_agent=agent, input="What's your name", context=user_info)


print("\n[RUNNER.RUN_SYNC]")
print(Runner.run_sync)

print('\n[RESULT]')
print(result)

print("\n[RESULT.FINAL_OUTPUT]")
print("result:",result.final_output)
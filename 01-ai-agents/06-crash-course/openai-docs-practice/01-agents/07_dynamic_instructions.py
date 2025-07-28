from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, enable_verbose_stdout_logging, RunContextWrapper
import asyncio
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()
set_tracing_disabled(disabled=False)
enable_verbose_stdout_logging()

@dataclass
class UserContext:
    name:str
    age:int

def dynamic_instructions(ctx:RunContextWrapper, agent: Agent[UserContext]) -> str:
    return f"The username is {ctx.context.name} greet him."


async def main():

    external_client = AsyncOpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )

    agent = Agent(
        name="Assistant",
        instructions=dynamic_instructions,
        model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client),

    )

    userInfo = UserContext(name="Huzair", age=20)

    result = await Runner.run(
        starting_agent=agent,
        input="Hello",
        context=userInfo
        )
    
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())


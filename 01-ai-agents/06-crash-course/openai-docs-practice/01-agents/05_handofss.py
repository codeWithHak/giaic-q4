from agents import Agent, Runner, enable_verbose_stdout_logging, RunContextWrapper,function_tool, set_default_openai_api
import asyncio
from dataclasses import dataclass
from dotenv import load_dotenv

set_default_openai_api("chat_completions")

load_dotenv()
enable_verbose_stdout_logging()

async def main():



    physics_agent = Agent(
        name="Physics Agent",
        instructions="Handle any query related to physics",
        handoff_description="handoff to this agent if query is related to physics"
    )

    maths_agent = Agent(
        name="Maths Agent",
        instructions="Handle any query related to maths",
        handoff_description="handoff to this agent if query is related to maths"
    )



    triage_agent = Agent(
        name="Triage Agent",
        instructions=("Help the user with their queries"
                      "If user asks about maths handoff to the math agents"
                      "If user asks about physics handoff to the physics agents"
        ),
        handoffs=[maths_agent, physics_agent]
    )

    result = await Runner.run(
        starting_agent=triage_agent,
        input="What is 2+2",
        )
    
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())


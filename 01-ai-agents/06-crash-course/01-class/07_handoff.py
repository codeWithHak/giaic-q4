from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, set_tracing_disabled,enable_verbose_stdout_logging, Handoff, handoff
from dotenv import load_dotenv
import os
from rich import print

set_tracing_disabled(disabled=True)
load_dotenv()

enable_verbose_stdout_logging()

balance = 11

def check_memebership(ctx,agent):
    return True if balance > 10 else False


external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("BASE_URL")
)


math_agent = Agent(
    name="Math Agent",
    instructions="Handle math questions of user and respond accordigly.",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client),
    handoff_description="An agent for handling math related queries"
)


physics_agent = Agent(
    name="Physics Agent",
    instructions="Handle physics questions of user and respond accordigly.",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client),
    handoff_description="An agent for handling math related queries"
)

agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client),
    handoffs=
    [
        math_agent,
        handoff(
            agent=physics_agent,
            tool_name_override="Physics_Agent",
            tool_description_override="This tool handles all the queries related to physics",
            is_enabled=check_memebership
            )
    ],
    
)

user_input = input("Ask me anything: ")
result = Runner.run_sync(starting_agent=agent, input=user_input)

print("result:",result.final_output)

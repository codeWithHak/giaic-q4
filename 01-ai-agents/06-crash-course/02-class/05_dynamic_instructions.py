from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, set_tracing_disabled,enable_verbose_stdout_logging
from dotenv import load_dotenv
import os
from rich import print

set_tracing_disabled(disabled=True)
load_dotenv()



enable_verbose_stdout_logging()


def get_dynamic_prompt(ctx,agent) -> str:
    print("\n[CTX]",ctx)
    print("\n[AGENT]",agent)
    return "You are an amazing and friendly assistand that helps user in their quries in a friendly way!"

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("BASE_URL")
) 

agent = Agent(
    name="assistant",
    instructions=get_dynamic_prompt,
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)
    
)

result = Runner.run_sync(starting_agent=agent, input="Yeahhh budyyyy light weight babyyyyy!!!!")

print("result:",result.final_output)
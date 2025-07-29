from agents import (
    Agent,
    Runner,
    enable_verbose_stdout_logging,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    GuardrailFunctionOutput,
    )


from dotenv import load_dotenv
import os
from pydantic import BaseModel

set_tracing_disabled(disabled=False)
enable_verbose_stdout_logging()

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)


class MathHomeWorkOutput(BaseModel):
    is_math_homework:bool
    reasoning:str

guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions="Check if user is asking about math homework",
    output_type=MathHomeWorkOutput
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash",openai_client=external_client),

)

result = Runner.run_sync(starting_agent=agent, input="Hello")
print(result.final_output)
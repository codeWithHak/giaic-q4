from agents import (
    Agent,
    Runner,
    # enable_verbose_stdout_logging,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    GuardrailFunctionOutput,
    input_guardrail,
    output_guardrail,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    )


from dotenv import load_dotenv
import os
from pydantic import BaseModel
import asyncio
from rich import print 

set_tracing_disabled(disabled=False)
# enable_verbose_stdout_logging()

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)


class MathHomeWorkOutput(BaseModel):
    is_math_homework:bool
    reasoning:str

class PhysicsHomeWorkOutput(BaseModel):
    is_physics_homework:bool
    reasoning:str

class MessageOutput(BaseModel):
    response:str

input_guardrail_agent = Agent(
    name="Input Guardrail Agent",
    instructions="Check if user is asking about math homework",
    output_type=MathHomeWorkOutput,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash",openai_client=external_client),
)

output_guardrail_agent = Agent(
    name="Output Guardrail Agent",
    instructions="Check if user is asking about physics homework",
    output_type=PhysicsHomeWorkOutput,
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash",openai_client=external_client),
)

@input_guardrail
async def math_guardrail(ctx, agent, input):
    result = await Runner.run(input_guardrail_agent, input)
    print("1- Input Guardrail Final Output: ",result.final_output)
    print('2- INPUT:', input)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework
    )

@output_guardrail
async def physics_guardrail(ctx, agent, output):
    result = await Runner.run(output_guardrail_agent, output.response)
    print("INPUT:", output)
    print("Output Guardrail Final Output:", result.final_output)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_physics_homework
    )

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash",openai_client=external_client),
    input_guardrails=[math_guardrail],
    output_guardrails=[physics_guardrail],
    output_type=MessageOutput
)


async def main():
    try:
        result = await Runner.run(starting_agent=agent, input="what is newtons first law of motion")
        print("Main Agent Final Output:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("I can't tell you anything related to math")
    except OutputGuardrailTripwireTriggered:
        print("I can't tell you anything related to physics")

asyncio.run(main())
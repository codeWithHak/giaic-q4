from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    set_tracing_disabled,
    AsyncOpenAI,
    OpenAIChatCompletionsModel

)


from dotenv import load_dotenv
import os
from pydantic import BaseModel
import asyncio

set_tracing_disabled(disabled=False)
# enable_verbose_stdout_logging()

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)



class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

guardrail_agent = Agent( 
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)
)


@input_guardrail
async def math_guardrail( 
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=result.final_output.is_math_homework,
    )


agent = Agent(  
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail],
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)
)

async def main():
    # This should trip the guardrail
    try:
        await Runner.run(agent, "Hello, which products do you guys have?")
        print("Guardrail didn't trip - this is unexpected")

    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")

asyncio.run(main())
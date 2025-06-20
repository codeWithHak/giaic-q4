from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI, Runner, set_tracing_disabled
# from openai import AsyncOpenAI

external_client = AsyncOpenAI(
    api_key = os.getenv("")
)
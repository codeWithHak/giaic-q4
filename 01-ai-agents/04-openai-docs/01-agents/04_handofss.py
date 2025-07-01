from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
import os

set_tracing_disabled(disabled=True)
load_dotenv()

API_KEY=os.getenv("API_KEY")
BASE_URL=os.getenv("BASE_URL")

if not API_KEY:
    raise KeyError("API KEY NOT FOUND!")

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

expert_linkedin_research_agent=Agent(
    name="Expert LinkedIn Content Topic Researcher",
    instructions="You are a expert researcher who researches and find a specific topic for user that they can create a post on, for LinkedIn",
    handoff_description="Handle all querries related to researching a topic for LinkedIn post",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client),
)


expert_linkedin_writer_agent=Agent(
    name="Expert LinkedIn Content Writer",
    instructions="You are an expert content writer who writes LinkedIn posts on any topic that user gives",
    handoff_description="Handle all querries related writing a post for LinkedIn",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client),
)

tirage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "Resolve user's querry"
        "If they ask for any topic to write a LinkedIn post on, handoff to Expert LinkedIn Content Topic Researcher agent"
        "If they ask to write a LinkedIn post, handoff to Expert LinkedIn Content Writer agent"
        ),
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client),
    handoffs=[expert_linkedin_research_agent,expert_linkedin_writer_agent],
)

result = Runner.run_sync(
    starting_agent=tirage_agent,
    input="Write a LinkedIn post on The Evolving Skillset: What's One New Skill You're Actively Learning (or Planning to Learn) to Stay Relevant in 2024 and Beyond?"
)

print(result.final_output)
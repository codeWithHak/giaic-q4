from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, AgentOutputSchema
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from dataclasses import dataclass
import asyncio

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY=os.getenv("API_KEY")
BASE_URL=os.getenv("BASE_URL")

client = AsyncOpenAI(
    api_key = API_KEY,
    base_url= BASE_URL
)

# @dataclass
# class TournamentPartcipants(BaseModel):
#     total_participants:int
#     starting_from:str
#     ending_on:str
#     is_registration_open:bool
    
class Develpoer(BaseModel):
    is_coding_related: bool
    is_technical_person: bool
    reason:str
    
class CalendarEvent(BaseModel):
    name: str|list[str]
    date: str|list[str]
    participants: str|list[str]
    
    
agent = Agent(
    name="Tournament Marketing Agent",
    # instructions="You can extract out from the statement that wether the person talking is technical or not and wether the statement is coding related or not",
    instructions="Extract calender events from text",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client),
    output_type=AgentOutputSchema(output_type=CalendarEvent)
    
)


async def main():
    result = await Runner.run(starting_agent=agent, input="Baqra Eid was on 12 july 2025, and ramzan will be starting from feb 22 2026")
    print(result.final_output)
    
asyncio.run(main())
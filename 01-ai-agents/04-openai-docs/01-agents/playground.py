#type:ignore
"""1-Context """

# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, RunContextWrapper
# from dotenv import load_dotenv
# import os
# from dataclasses import dataclass
# import asyncio

# load_dotenv()
# set_tracing_disabled(disabled=True)

# API_KEY=os.getenv("API_KEY")
# BASE_URL=os.getenv("BASE_URL")

# client = AsyncOpenAI(
#     api_key = API_KEY,
#     base_url= BASE_URL
# )

# @dataclass
# class UserInfo:
#     name:str
#     age:int
#     email:str

# @function_tool
# async def fetch_user_details(wrapper:RunContextWrapper[UserInfo]):
#     """Returns user name, age and email"""
#     # if we dont return the email but have email in user info what happens?
#     # agent loop will still call this (fetch_user_details) tool, it will see there's only name and age return not email
#     # so it will not get the email from agent and hence ll won't get mail so it will not give output of what's email of user!
#     return wrapper.context.name, wrapper.context.age, 

# agent = Agent(
#     name="Assistant",
#     instructions="You are a helpful assistant",
#     model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client),
#     tools=[fetch_user_details]
# )

# user_info = UserInfo(name="Huzair",age=19, email="huzairahmedkhan@gmail.com")

# async def main():
#     result = await Runner.run(starting_agent=agent, input="What's the email of user", context=user_info)
#     print(result.final_output)
    
# asyncio.run(main())





"""2-Dynamic Instructions"""

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
    
class Employee(BaseModel):
    name:str
    department:str
    salary:int
    experience:str
    
    
agent = Agent(
    name="Employee Sorting Agent",
    instructions="Extract employee from text and sort it in a dict, then add all dicts in a list. add line break after every dict",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client),
    output_type=AgentOutputSchema(output_type=list[Employee], strict_json_schema=True)
    
)


async def main():
    result = await Runner.run(
        starting_agent=agent,
        input="""
        John Sales 65000 3 years
        Finance Sarah 4 years 72000
        Marketing Ahmed 2yrs 59000
        Emily HR 1 year 40000
        Tech Hassan 95000 6
        Samira Legal 3 67000
        67000 Zainab HR 2 years
        Developer Adnan 5 years 105000
        Production Zara 78000 4
        3yrs Sales Waqas 62000
        IT Bilal 87000 6 years
        Ayesha 53000 1yr Content
        Admin Umar 70000 3years
        DevOps Moiz 89000 5
        Asma QA 2y 61000
        Support 46000 Farhan 1.5yrs
        Fatima Legal 3 years 71000
        Engineering Ali 94000 7yrs
        Sara HR 52000 2 years
        2yrs Rizwan Tech 86000
        Mariam Sales 4years 68000
        Support Yasir 61000 3y
        Areeba HR 47000 1yr
        IT Hina 5 88000
        HR Sana 2.5yrs 53000
        Shayan Marketing 3 67000
        Accountancy Hammad 73000 4.5years
        Amna 4 Marketing 64000
        CustomerCare Daniyal 3yrs 60000
        HR Usman 56000 1 year
        Faizan Support 2 50000
        Legal Nimra 4.5y 71000
        Tech Adeel 5yrs 91000
        Anum Admin 2yrs 49000
        Kiran 3 Content 58000
        R&D Talha 6 years 99000
        Bilquis Finance 2y 63000
        Zoya HR 1.5yrs 45000
        Software Ehsan 87000 6
        Hamza QA 3y 69000
        Rida Marketing 54000 2yrs
        HR Arham 48000 1 year
        Finance Maaz 4y 76000
        Tariq Tech 91000 5
        Support Maira 2.5yrs 61000
        Aliya Legal 70000 3yrs
        Waleed Sales 3 65000
        Urooj 1y HR 43000
        Faraz Content 5yrs 83000
        3yrs Osama Admin 61000
        Yahya Engineering 6yrs 99000
        Production Huda 3.5y 74000
        Haris QA 4yrs 67000
        Finance Iqra 2yrs 59000""")
    print(result.final_output)
    
asyncio.run(main())
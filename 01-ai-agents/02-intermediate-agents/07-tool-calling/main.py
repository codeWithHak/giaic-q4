#ignore:type

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()
set_tracing_disabled(disabled=True)


API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)


@function_tool
def weather(city:str) -> str:
    """
    Give weather of the city based on city

    Args:
        city (string): name of a city
    """
    return f"Weather in {city} is 22C"
   
@function_tool     
def get_employees_details():
    """
    User will tell you the name of an employee and ask for deatils on that employee you will look into  
    employees_details and store that info in info variable then give the info to user that he wants, also you can give him whole emplyees data if he ask, just follow his instructions if they are related to company workers or employees, he could ask for anything inside employees_details search for key and give him the vlaue he needs.
    """
    info = ""
    
    employees_details = [
    {
        "name": "Adeel Raza",
        "salary": 120000,
        "years_with_company": 5,
        "designation": "Senior Software Engineer",
        "department": "Backend Development"
    },
    {
        "name": "Hina Tariq",
        "salary": 95000,
        "years_with_company": 3,
        "designation": "Data Analyst",
        "department": "Data & Analytics"
    },
    {
        "name": "Imran Qureshi",
        "salary": 135000,
        "years_with_company": 7,
        "designation": "DevOps Lead",
        "department": "Infrastructure & Cloud"
    },
    {
        "name": "Sara Khan",
        "salary": 88000,
        "years_with_company": 2,
        "designation": "UI/UX Designer",
        "department": "Design"
    },
    {
        "name": "Bilal Ahmed",
        "salary": 110000,
        "years_with_company": 4,
        "designation": "Full Stack Developer",
        "department": "Web Engineering"
    },
    {
        "name": "Fatima Sheikh",
        "salary": 102000,
        "years_with_company": 6,
        "designation": "Project Manager",
        "department": "Product & Operations"
    }
]   
    return "Here's the info you asked for {info}"

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=external_client),
    tools=[weather,get_employees_details]
)

user_input = input("Ask me anything: ")
async def main():
    result = await Runner.run(starting_agent=agent, input=user_input)
    print(result.final_output)
    
asyncio.run(main())



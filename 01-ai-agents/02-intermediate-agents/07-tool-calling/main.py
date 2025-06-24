#type:ignore
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
def weather(city: str) -> str:
    """
    Give weather of the city based on city

    Args:
        city (string): name of a city
    """
    return f"Weather in {city} is 22C"

@function_tool
def get_employees_details(name: str = None) -> str:
    """
    Retrieve details of an employee by name or return all employees' details if no name is provided.
    Search the employees_details list for the given name and return the matching employee's information.
    If no match is found, return a message indicating so. If no name is provided, return all employees' data.

    Args:
        name (string, optional): Name of the employee to search for. If not provided, return all employees.
    """
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

    if name:
        # Search for employee by name (case-insensitive)
        for employee in employees_details:
            if employee["name"].lower() == name.lower():
                return (
                    f"Employee Details:\n"
                    f"Name: {employee['name']}\n"
                    f"Salary: {employee['salary']}\n"
                    f"Years with Company: {employee['years_with_company']}\n"
                    f"Designation: {employee['designation']}\n"
                    f"Department: {employee['department']}"
                )
        return f"No employee found with the name '{name}'."
    else:
        # Return all employees if no name is provided
        result = "All Employees:\n"
        for employee in employees_details:
            result += (
                f"\nName: {employee['name']}\n"
                f"Salary: {employee['salary']}\n"
                f"Years with Company: {employee['years_with_company']}\n"
                f"Designation: {employee['designation']}\n"
                f"Department: {employee['department']}\n"
                "-------------------\n"
            )
        return result



agent = Agent(
    name="Assistant",
    instructions=(
        "You are a helpful assistant specializing in providing information about company employees and weather. "
        "Use the 'get_employees_details' tool to answer queries about employee details, such as their name, salary, designation, or department. "
        "If the user asks for an employee's details, extract the name from their input and pass it to the tool. "
        "If the user asks for all employees, call the tool without a name. "
        "For weather-related queries, use the 'weather' tool."
    ),
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=external_client),
    tools=[weather, get_employees_details]
)

user_input = input("Ask me anything: ")

async def main():
    result = await Runner.run(starting_agent=agent, input=user_input)
    print(result.final_output)

asyncio.run(main())
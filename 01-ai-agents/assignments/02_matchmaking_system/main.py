from agents import Agent, Runner, function_tool, WebSearchTool
from dotenv import load_dotenv
import os 
from dataclasses import dataclass
load_dotenv()
@dataclass
class User:
    name:str
    age:int
    salary:int

@function_tool
def get_user_data(age:int,salary:int):        
    user_data = [    
        {"name":"Huzair Ahmed Khan", "age":19, "salary":1500000},
        {"name":"Huzaifa Farooqui", "age":26, "salary":500000},
        {"name":"Shah Rukh Khan", "age":52, "salary":150000000}
        ]
    
    for user in user_data:
        if user["age"] > age and user["salary"] < salary:
            user_data.remove(user)
    
    return user_data            


match_making_agent = Agent(
    name="Match Making Agent",
    instructions="you are a match maker agent please find relevant matches for user",
    tools=[get_user_data, WebSearchTool()]
)

result = Runner.run_sync(
    starting_agent=match_making_agent,
    input="Find a match for me who earns more than 10000 PKR and is under 25, also tell me some detailed info about that person from his linkedin",
)

print(result.final_output)
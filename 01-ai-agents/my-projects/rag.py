from agents import Agent, Runner, FileSearchTool
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")



user_info_agent = Agent(
    name="User Info Agent",
    instructions="""
    You will handle the querries of client for this user, client will ask you anything about this suer like does this user attend webinars? does he listens to music? 
    what he likes what he dosent etc.
    You will get emails to extratct data.
    You will respond and also give reference like from which email you found that info?
    And what was the date of that email?
""",
    tools=[FileSearchTool(
            max_num_results=3,
            vector_store_ids=["vs_68878886b31c8191b482ea4d11b6134c"],
        )],
    model="gpt-4o-mini"
)
user_input = input("Ask anything about this user: ")
result = Runner.run_sync(user_info_agent, user_input)
print(result.final_output)

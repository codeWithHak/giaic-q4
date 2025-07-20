from agents import Agent, Runner, AgentOutputSchema, enable_verbose_stdout_logging, set_default_openai_api
from dotenv import load_dotenv
from pydantic import BaseModel
from rich import print 
import agents.result

load_dotenv()
enable_verbose_stdout_logging()
set_default_openai_api("chat_completions")

class JsonOutput(BaseModel):
    result:dict[str,str]

agent = Agent(
    name="Assistant",
    instructions="you're a helpful assistant",
    
    # You can define any type of output you wnat from the llm e.g:
    
    # output_type=int
    # output_type=str
    # output_type=AgentOutputSchema(dict[str,str], strict_json_schema=False)
)

result = Runner.run_sync(starting_agent=agent, input="What is 2+2")

print(result)
print(type(result))


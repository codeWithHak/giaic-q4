from agents import Agent, Runner, AgentOutputSchema, enable_verbose_stdout_logging, set_default_openai_api
from dotenv import load_dotenv
from pydantic import BaseModel
from rich import print 


load_dotenv()
enable_verbose_stdout_logging()
set_default_openai_api("chat_completions")


# !!! ----- 2 ------- !!! advanced type
class BattingStats(BaseModel):
    batsman_name: str
    highest_score: int
    average: float

agent = Agent(
    name="Assistant",
    instructions="you're a helpful assistant",
    
    # You can define any type of output you wnat from the llm e.g:
    
    # output_type=int
    # output_type=str
    
    # !!! ----- 2 ------- !!! advanced tpes
    output_type=list[BattingStats]
)

# result = Runner.run_sync(starting_agent=agent, input="What is 2+2")

# !!! ----- 2 ------- !!!
result = Runner.run_sync(starting_agent=agent, input="Ahmed Shehzad scored 99 runs in his last psl match and after that he scored 50 runs in 3 more matches, Babar Azam scored 3 consecutive centuroes against windies with the highest score of 120 and then scored 3 ducks against Australia ")


# if we just print result.final_output like this,
# print(result.final_output)

# we will get a list of instances like: 
#[
#    BattingStats(batsman_name='Ahmed Shehzad', highest_score=99, average=62.75),
#    BattingStats(batsman_name='Babar Azam', highest_score=120, average=60.0)
#]

# But we want list of dicts so we use .model_dump() for each instance and get result in dict. 
print([res.model_dump() for res in result.final_output])
print(type(result))


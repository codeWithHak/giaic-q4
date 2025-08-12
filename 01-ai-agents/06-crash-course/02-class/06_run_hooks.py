from agents import Agent, Runner,enable_verbose_stdout_logging, RunHooks, function_tool
from dotenv import load_dotenv
from rich import print

load_dotenv()

enable_verbose_stdout_logging()



spanish_translater_agent = Agent(
    name="Spanish Translator Agent",
    instructions="You're an expert Spanish language translator",
    model="gpt-4o-mini",
)




# @function_tool
# def spanish_translator(spanish_word:str, english_translation:str) -> str:
#     """
#     An expert spanish to english translator

#     Args: 
#         1- spanish_word(str): This will be the word user ask to translate from. 
#         1- english_word(str): This will be the word you will translate to in english.

#     Returns:
#         English translation of user query in short string 

#     """
#     return f"{spanish_word} in english is {english_translation}"


@function_tool
def translator(from_word:str, from_language:str) -> str:
    """
    An expert language translator.

    Pick word and language from user prompt, and unserstand which word user is trying to translate in which language.
    Then translate it and return a short string.

    Args: 
        1- from_word(str): This will be the word user ask to translate from.
        2- from_language(str): This will be the language user will ask to translate in. 

    Returns:
        Translation of from_word to (to_word) in the user defined (language) from from_language.

    """
    return f"{from_word} in (to_language) is (to_word)"



agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant",
    model="gpt-4o-mini",
    tools=[translator],
    handoffs=[spanish_translater_agent]
)

# class TestRunHooks(RunHooks):

#     async def on_agent_start(self,context,agent):
#         print(f"\n[ON_AGENT_START]")
        
#         print('\n[ON_AGENT_START_SELF]')
#         print(self)

#         print('\n[ON_AGENT_START_CONTEXT]')
#         print(context)

#         print('\n[ON_AGENT_START_AGENT]')
#         print(agent)


#     async def on_agent_end(self,context,agent,output):
#         print(f"\n[ON_AGENT_END]")

#         print('\n[ON_AGENT_END_SELF]')
#         print(self)

#         print('\n[ON_AGENT_END_CONTEXT]')
#         print(context)

#         print('\n[ON_AGENT_END_AGENT]')
#         print(agent)

#         print('\n[ON_AGENT_END_OUTPUT]')
#         print(output)


#     async def on_handoff(self,context,from_agent,to_agent):

#         print('\n[ON_HANDOFF]')

#         print('\n[ON_HANDOFF_SELF]')
#         print(self)

#         print('\n[ON_HANDOFF_CONTEXT]')
#         print(context)

#         print('\n[ON_HANDOFF_FROM_AGENT]')
#         print(from_agent)

#         print('\n[ON_HANDOFF_TO_AGENT]')
#         print(to_agent)



#     async def on_tool_start(self, context, agent, tool):
#         print('\n[ON_TOOL_START]')

#         print('\n[ON_TOOL_START_SELF]')
#         print(self)

#         print('\n[ON_TOOL_START_CONTEXT]')
#         print(context)

#         print('\n[ON_TOOL_START_AGENT]')
#         print(agent)

#         print('\n[ON_TOOL_START_TOOL]')
#         print(tool)
        
#         return await super().on_tool_start(context, agent, tool)
    
#     async def on_tool_end(self, context, agent, tool, result):
#         return await super().on_tool_end(context, agent, tool, result)


result = Runner.run_sync(starting_agent=agent, input="What is apple in spanish")

print("\n[Agent.tools]")
print(agent.tools)
print("\n[Agent.handoffs]")
print(agent.handoffs)
print("result:",result.final_output)
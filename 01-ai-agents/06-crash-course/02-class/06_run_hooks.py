from agents import Agent, Runner,enable_verbose_stdout_logging, RunHooks, function_tool
from dotenv import load_dotenv
from rich import print

load_dotenv()

enable_verbose_stdout_logging()



translater_agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant",
    model="gpt-4o-mini",
)


@function_tool
def spanish_translator():
    return "Spanish text"



agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant",
    model="gpt-4o-mini",
    tools=[translater_agent.as_tool(tool_name="Translator", tool_description="translates any language to english"), spanish_translator]
)

class TestRunHooks(RunHooks):
    async def on_agent_start(self,context,agent):
        print(f"\n[ON_AGENT_START]")
        
        print('\n[SELF]')
        print(self)

        print('\n[CONTEXT]')
        print(context)

        print('\n[AGENT]')
        print(agent)
    async def on_agent_end(self,context,agent,output):
        print(f"\n[ON_AGENT_END]")

        print('\n[SELF]')
        print(self())

        print('\n[CONTEXT]')
        print(context)

        print('\n[AGENT]')
        print(agent)

        print('\n[OUTPUT]')
        print(output)


    async def on_tool_start(self, context, agent, tool):
        print('\n[ON_TOOL_START]')

        print('\n[SELF]')
        print(self)

        print('\n[CONTEXT]')
        print(context)

        print('\n[AGENT]')
        print(agent)

        print('\n[TOOL]')
        print(tool)
        
        return await super().on_tool_start(context, agent, tool)


result = Runner.run_sync(starting_agent=agent, input="What is apple in french", hooks=TestRunHooks())

print("result:",result.final_output)
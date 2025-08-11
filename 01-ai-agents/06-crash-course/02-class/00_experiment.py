from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from rich import print
import requests

set_tracing_disabled(True)

external_client = AsyncOpenAI(
    api_key='AIzaSyA7lE_ZDwT55XAI9uA3chwsnJuwAojsORU',                          
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/')

model = OpenAIChatCompletionsModel(
    model='gemini-2.5-flash',
    openai_client=external_client,
)

@function_tool
async def get_weather_info(City: str) -> str:
    API_KEY = '75d45f2ed5abe7a4552ca63085165a8a'
    BASE_URL = f'https://api.openweathermap.org/data/2.5/weather?q={City}&appid={API_KEY}'
    response = await requests.get(BASE_URL).json()
    return response

agent = Agent(name='test', instructions='You are a helpful assistant that can answer questions and help with tasks.',
              model=model, tools=[get_weather_info])
user_input = input('Enter a prompt: ')

result = Runner.run_sync(agent, user_input)

print(result.final_output)
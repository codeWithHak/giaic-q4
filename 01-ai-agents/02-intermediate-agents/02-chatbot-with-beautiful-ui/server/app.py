from flask import Flask, jsonify, request
from flask_cors import CORS
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
from asgiref.wsgi import WsgiToAsgi
import os

load_dotenv()
set_tracing_disabled(disabled=True)

client = AsyncOpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model=os.getenv("MODEL"), openai_client=client),
)

app = Flask(__name__)
CORS(app)

@app.route('/api/home', methods=['POST'])
async def home():
    data = request.get_json()
    result = await Runner.run(agent, data['query'])
    return jsonify({"message": result.final_output})

if __name__ == "__main__":
    import uvicorn
    asgi_app = WsgiToAsgi(app)
    uvicorn.run(asgi_app, host="127.0.0.1", port=8080)
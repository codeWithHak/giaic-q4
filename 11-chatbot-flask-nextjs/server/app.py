from flask import Flask, jsonify
from flask_cors import  CORS
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY=os.getenv("API_KEY")
BASE_URL=os.getenv("BASE_URL")
MODEL=os.getenv("MODEL")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),  
)

result = Runner.run_sync(
    starting_agent=agent,
    input="How are you"
)

print(result.final_output)

# app = Flask(__name__)
# CORS(app)


# @app.route('/api/home')
# def home():
#     return jsonify({
#         "message":"hello from server"
#     })
    
# if __name__ == "__main__":
#     app.run(debug=True, port=8080)
    
# 1- change port, 2- remove app.run() and play with it, 3- play with CORS, 4- play with jsonify 
# import nest_asyncio
from dotenv import load_dotenv
import json
import requests
import os
# nest_asyncio.apply()
load_dotenv() 

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")
URL = os.getenv("URL")

response = requests.post(
    url = URL,
    headers={
        "Authorization":f"Bearer {OPENROUTER_API_KEY}"
    },
    data=json.dumps({
        "model":MODEL,
        "messages":[
            {
                "role":"user",
                "content":"What is the capital of Pakistan"
            }
        ]
    })
)

print(response.json()['choices'][0]['message']['content'])
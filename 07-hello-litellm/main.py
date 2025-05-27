from litellm import completion
import os
from dotenv import load_dotenv

load_dotenv()
## set ENV variables
os.environ["BASE_URL"] = os.getenv("BASE_URL")
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
def call_mistral():
    user_input = input("Ask me anything: ")

    response = completion(
      model="openrouter/mistralai/mistral-7b-instruct",
      messages=[{ "content": user_input,"role": "user"}]
    )

    print(response['choices'][0]['message']['content'])
    
call_mistral()
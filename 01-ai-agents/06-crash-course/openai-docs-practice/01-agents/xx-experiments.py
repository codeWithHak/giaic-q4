# tool testing
from rich import print
# import json
from google import genai
import os
# with open("mails.json", "r") as f:
#     data = json.load(f)


from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")




client = genai.Client()

result = client.models.embed_content(
        model="gemini-embedding-001",
        contents="What is the meaning of life?")

print(result.embeddings)





# starting_range = 0
# ending_range = 20
# chunk = []

# with open("summaries.json", "w") as f:
#     while ending_range <= len(data):
        
#         for i in range(starting_range,ending_range):
#             chunk.append(data[i])
            
#         for mail in chunk:
#             f.write(json.dumps(mail) + "\n")
            
#         chunk.clear()
#         starting_range += 20
#         ending_range += 20
    

    
# tool testing
from rich import print
import json

with open("mails.json", "r") as f:
    data = json.load(f)


starting_range = 0
ending_range = 20
chunk = []

with open("summaries.json", "w") as f:
    while ending_range <= len(data):
        
        for i in range(starting_range,ending_range):
            chunk.append(data[i])
            
        for mail in chunk:
            f.write(json.dumps(mail) + "\n")
            
        chunk.clear()
        starting_range += 20
        ending_range += 20
    

    
import json



with open("api_response.json", 'r') as f:
    data = json.load(f)

for item in data:
    print(len(item["rows"]))
    
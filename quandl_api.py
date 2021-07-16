import json

with open("config.json") as json_data_file:
    data = json.load(json_data_file)

key = data["api_key"]
endpoint = data["endpoint"]
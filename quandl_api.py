import json
import requests
import quandl

# load configs
with open("config.json") as json_data_file:
    data = json.load(json_data_file)

quandl.ApiConfig.api_key = data["api_key"]

# key = data["api_key"]
# endpoint = data["endpoint"]
# response = requests.get(endpoint + 'indicator_id=ZSFH&region_id =99999&api_key=' + key)

response = quandl.get_table('ZILLOW/DATA', indicator_id='ZSFH', region_id='99999')

print(response)
import mysql.connector
import json
import requests
import quandl
import numpy as np

# load configs
with open("config.json") as json_data_file:
    data = json.load(json_data_file)    

pw = data["mysql"]
key = data["api_key"]
endpoint = data["endpoint"]

# connect to MySQL
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = pw,
    database = "test"
)
cursor = db.cursor()
# cursor.execute("CREATE DATABASE test")

# run GET request on API
def getData(indicator,region):
    response = requests.get(endpoint +
    'indicator_id=' + indicator +
    '&region_id=' + region + '&api_key=' + key)
    return response.json()

# prints each column in datatable
homes = getData('ZSFH', '10001')

price_array = []
for home in homes['datatable']['data']:
    price_array.append(home[3])
    print(home)

np_price = np.array(price_array)
avg_price = np.average(np_price)

print(int(avg_price))

# DONE USING QUANDL MODULE:
# quandl.ApiConfig.api_key = data["api_key"]
# response = quandl.get_table('ZILLOW/DATA', indicator_id='ZSFH', region_id='10001')
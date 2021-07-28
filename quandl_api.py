import mysql.connector
import requests
import json
import numpy as np
from config import api_key, endpoint, mysql_pw
import quandl

# connect to MySQL
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = mysql_pw,
    database = "quandl"
)
cursor = db.cursor()
# cursor.execute("CREATE DATABASE quandl")

# run GET request on API
def getData(indicator,region):
    response = requests.get(endpoint 
    + 'indicator_id=' + indicator 
    + '&region_id=' + region 
    + '&api_key=' + api_key)
    return response.json()

# prints each column in datatable
homes = getData('ZSFH', '10001')

# save raw json file
with open('home_data.json', 'w') as f:
    json.dump(homes, f)

price_array = []
for home in homes['datatable']['data']:
    price_array.append(home[3]) # property price

# numpy calculations on price array
np_price = np.array(price_array)
avg_price = np.average(np_price)

print('Number of listings: %d' % np_price.size)
print('Average price: %d' % int(avg_price))

# DONE USING QUANDL MODULE:
# quandl.ApiConfig.api_key = data["api_key"]
# ZSFH, ZATT, Z2BR, Z3BR, Z4BR, Z5BR
quandl.ApiConfig.api_key = api_key
response = quandl.get_table('ZILLOW/DATA', indicator_id='ZSFH', region_id='90210')
# print(response)

response = quandl.get_table('ZILLOW/INDICATORS')
# print(response)

response = quandl.get_table('ZILLOW/REGIONS')
# print(response)
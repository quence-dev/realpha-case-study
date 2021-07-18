import mysql.connector
import json, requests
import quandl

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

response = requests.get(endpoint + 'indicator_id=ZSFH&region_id=10001&api_key=' + key)

# DONE USING QUANDL MODULE:
# quandl.ApiConfig.api_key = data["api_key"]
# response = quandl.get_table('ZILLOW/DATA', indicator_id='ZSFH', region_id='10001')

print()
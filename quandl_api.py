import quandl
import mysql.connector
import json
import datetime

# load configs
with open("config.json") as json_data_file:
    data = json.load(json_data_file)

quandl.ApiConfig.api_key = data["api_key"]
pw = data["mysql"]

# connect to MySQL
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = pw,
    database = "test"
)

cursor = db.cursor()
# cursor.execute("CREATE DATABASE test")

# key = data["api_key"]
# endpoint = data["endpoint"]
# response = requests.get(endpoint + 'indicator_id=ZSFH&region_id =99999&api_key=' + key)

response = quandl.get_table('ZILLOW/DATA', indicator_id='ZSFH', region_id='10001')

print(response)
import mysql.connector
from config import mysql_pw
import json

# connect to MySQL
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = mysql_pw,
    database = "allrecipes"
)
cursor = db.cursor()

with open("data.json") as json_data_file:
    data = json.load(json_data_file)

# cursor.execute("CREATE DATABASE allrecipes")
# cursor.execute("CREATE TABLE recipes (id int PRIMARY KEY AUTO_INCREMENT, title TEXT, summary TEXT, rating FLOAT, rating_count INT, url TEXT, author VARCHAR(50))")
# for items in data:
#     cursor.execute("INSERT INTO recipes(title, summary, rating, rating_count, url, author) VALUES (%s, %s, %s, %s, %s, %s)", 
#     (items['title'], items['summary'], items['rating'], items['rating_count'], items['url'], items['author']))

cursor.execute('SELECT * FROM recipes')

for x in cursor:
    print(x)
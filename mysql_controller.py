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

# cursor.execute('SELECT id, title, rating FROM recipes WHERE rating > 4.8')

# for x in cursor:
#     print(x)

cursor.execute('CREATE TABLE recipe_details (recipe_id int PRIMARY KEY, FOREIGN KEY(recipe_id) REFERENCES recipes(id), prep VARCHAR(20), cook VARCHAR(20), add VARCHAR(20), total VARCHAR(20), servings INT, yield VARCHAR(20), ingredients TEXT, directions TEXT)')
db.commit()
# for items in data:
#     print(items['metadata']['additional'])
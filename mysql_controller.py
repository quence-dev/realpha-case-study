from logging import currentframe
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
    # cursor.execute("INSERT INTO recipes(title, summary, rating, rating_count, url, author) VALUES (%s, %s, %s, %s, %s, %s)", 
    # (items['title'], items['summary'], items['rating'], items['rating_count'], items['url'], items['author']))

# cursor.execute('CREATE TABLE recipe_stats (recipeID int PRIMARY KEY NOT NULL AUTO_INCREMENT, FOREIGN KEY (recipeID) REFERENCES recipes(id), prep VARCHAR(20), cook VARCHAR(20), additional VARCHAR(20), total VARCHAR(20), servings INT, yield TEXT)')
# for items in data:
    # cursor.execute("INSERT INTO recipe_stats(prep, cook, additional, total, servings, yield) VALUES (%s,%s,%s,%s,%s,%s)", (items['metadata']['prep'], items['metadata']['cook'], items['metadata']['additional'], items['metadata']['total'], int(items['metadata']['servings']), items['metadata']['yield']))

# cursor.execute('CREATE TABLE directions (recipeID int PRIMARY KEY NOT NULL, FOREIGN KEY (recipeID) REFERENCES recipes(id), direction TEXT, step INT)')
# cursor.execute('CREATE TABLE ingredients (recipeID int PRIMARY KEY NOT NULL, FOREIGN KEY (recipeID) REFERENCES recipes(id), ingredient TEXT)')

# cursor.execute('SELECT id, title, rating FROM recipes WHERE rating > 4.8')

# cursor.execute('SELECT * FROM recipe_stats')
# for x in cursor:
#     print(x)

# for items in data:
#     for i in items['metadata']['ingredients']:
#         cursor.execute("INSERT INTO ingredients(ingredient) VALUES (%s)", (i))

Q1 = "INSERT INTO recipes(title, summary, rating, rating_count, url, author) VALUES (%s, %s, %s, %s, %s, %s)"
Q2 = "INSERT INTO recipe_stats(recipeID, prep, cook, additional, total, servings, yield) VALUES (%s,%s,%s,%s,%s,%s,%s)"
Q3 = "INSERT INTO ingredients(recipeID, ingredient) VALUES (%s, %s)"
Q4 = ""

for x, items in enumerate(data):
    cursor.execute(Q1, (items['title'], items['summary'], items['rating'], items['rating_count'], items['url'], items['author']))
    last_id = cursor.lastrowid
    cursor.execute(Q2, (last_id, items['metadata']['prep'], items['metadata']['cook'], items['metadata']['additional'], items['metadata']['total'], int(items['metadata']['servings']), items['metadata']['yield']))

db.commit()
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
# cursor.execute('CREATE TABLE recipe_stats (recipeID int PRIMARY KEY NOT NULL AUTO_INCREMENT, FOREIGN KEY (recipeID) REFERENCES recipes(id), prep VARCHAR(20), cook VARCHAR(20), additional VARCHAR(20), total VARCHAR(20), servings INT, yield TEXT)')
# cursor.execute('CREATE TABLE directions (recipeID int NOT NULL, FOREIGN KEY (recipeID) REFERENCES recipes(id), direction TEXT, step INT)')
# cursor.execute('CREATE TABLE ingredients (recipeID int NOT NULL, FOREIGN KEY (recipeID) REFERENCES recipes(id), ingredient TEXT)')

Q1 = "INSERT INTO recipes(title, summary, rating, rating_count, url, author) VALUES (%s, %s, %s, %s, %s, %s)"
Q2 = "INSERT INTO recipe_stats(recipeID, prep, cook, additional, total, servings, yield) VALUES (%s,%s,%s,%s,%s,%s,%s)"
Q3 = "INSERT INTO ingredients(recipeID, ingredient) VALUES (%s, %s)"
Q4 = "INSERT INTO directions(recipeID, direction, step) VALUES (%s,%s,%s)"

# performs insert of data into tables
# for items in data:
#     cursor.execute(Q1, (items['title'], items['summary'], items['rating'], items['rating_count'], items['url'], items['author']))
#     last_id = cursor.lastrowid
#     cursor.execute(Q2, (last_id, items['metadata']['prep'], items['metadata']['cook'], items['metadata']['additional'], items['metadata']['total'], int(items['metadata']['servings']), items['metadata']['yield']))
#     for i in items['metadata']['ingredients']:
#         cursor.execute(Q3, (last_id, i))
#     for count, i in enumerate(items['metadata']['directions']):
#         cursor.execute(Q4, (last_id, i, count+1))

# select all recipe titles and ingredients
S1 = 'SELECT title, ingredient FROM recipes JOIN ingredients ON recipes.id = ingredients.recipeID'

# show recipes with rating above 4.8
S2 = 'SELECT rating, title FROM recipes WHERE rating > 4.8'

# show recipes and their directions
S3 = 'SELECT title, step, direction FROM recipes JOIN directions ON recipes.id = directions.recipeID'

# show recipes that make more than 10 servings
S4 = 'SELECT title, servings, yield FROM recipes JOIN recipe_stats ON recipes.id = recipe_stats.recipeID WHERE servings > 10'

# show recipes with no additional time
S5 = 'SELECT id, title, total FROM recipes JOIN recipe_stats ON recipes.id = recipe_stats.recipeID WHERE additional IS NULL'

# update table to treat empty strings as null
# U1 = 'UPDATE recipe_stats SET additional = NULL WHERE additional = ""'
# cursor.execute(U1)

cursor.execute(S5)
for x in cursor:
    print(x)
import mysql.connector
from config import mysql_pw

# connect to MySQL
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = mysql_pw,
    database = "allrecipes"
)
cursor = db.cursor()

# cursor.execute("CREATE DATABASE allrecipes")
# cursor.execute("CREATE TABLE recipes (id int PRIMARY KEY AUTO_INCREMENT, title VARCHAR(50), summary TEXT, rating FLOAT, rating_count INT, url TEXT, author VARCHAR(50))")

import mysql.connector
from config import mysql_pw

# connect to MySQL
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = mysql_pw,
    # database = "quandl"
)
cursor = db.cursor()
# cursor.execute("CREATE DATABASE quandl")
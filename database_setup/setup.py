import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
  # database="mydatabase"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE mydatabase")
mydb.database = "mydatabase"
mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE customers (VARCHAR(255), address VARCHAR(255))")
# mycursor.execute("SHOW DATABASES")
mycursor.execute("SHOW TABLES")


for x in mycursor:
  print(x) 
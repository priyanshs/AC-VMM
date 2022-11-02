"""
The following code connects to the local server and creates the database and schema
"""


import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
  # database="mydatabase"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE mydatabase")
mycursor.execute("USE mydatabase")
mydb.database = "mydatabase"
mycursor = mydb.cursor()


table_schema ="""CREATE TABLE `grading` (
	`s_id` INT,
	`vm_id` INT,
	`assign_id` INT,
	`time_vm` INT,
	`no_launches` INT,
	`activity_1` INT,
	`activity_2` INT,
	`activity_3` INT,
	`static_dist` INT,
	`grading_time` INT,
	`dynamic_dist` INT,
	`cheat_label` INT,
	`marks` INT,        
 	PRIMARY KEY (`s_id`,`assign_id`)
);"""

mycursor.execute(table_schema)
# # mycursor.execute("SHOW DATABASES")
# mycursor.execute("SHOW TABLES")

# for x in mycursor:
#   print(x) 

#   mycursor.execute("DESCRIBE grading")

# for x in mycursor:
#   print(x) 
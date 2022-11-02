# The following code adds dummy values into the grading table 

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mydatabase",
)

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


mycursor = mydb.cursor()

sql = "INSERT INTO grading VALUES (%s, %s,%s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s);"
val = [
  ('01', '01', '01', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
  ('02', '01', '01', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
  ('03', '01', '01', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
  ('04', '01', '01', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
  ('05', '01', '01', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
  ('06', '01', '01', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
  ('07', '01', '01', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
  ('08', '01', '01', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
  ('09', '01', '01', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
  ('10', '01', '01', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
  ('11', '01', '01', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
  ('12', '01', '01', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
  ('13', '01', '01', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
]

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.") 
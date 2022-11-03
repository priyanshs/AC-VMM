import os
import shutil
import mysql.connector

# os.system("mkdir grading")
# os.system("mkdir grading/testing")
# os.system("mkdir grading/testing/input")
# os.system("mkdir grading/testing/output")


movdir = "code"
basedir = "grading"
# Walk through all files in the directory that contains the files to copy
for root, dirs, files in os.walk(movdir):
    # print( root, dirs, files )
    for filename in files:
        old_name = os.path.join( os.path.abspath(root), filename )
    
        file_n = root.split('/')[1] + ".py"

        # Initial new name
        new_name = os.path.join(basedir, file_n)
        shutil.copy(old_name, new_name)

basedir = "student-code/grading"
# print(os.path.abspath(basedir))
x = os.system("autograder run " + os.path.abspath(basedir) + "/ > /dev/null")


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mydatabase",
)
mycursor = mydb.cursor()

student_score = []
scorepath = basedir + "/results/"
for root, dirs, files in os.walk(scorepath):
    # print( root, dirs, files )
    for filename in files:
        with open(scorepath + filename, 'r') as fp:
            lines = fp.readlines()
            for row in lines:
                word = 'Result:'
                if row.find(word) != -1:
                    
                    upp = "UPDATE grading SET marks = "+row.split()[1].split('/')[0]+" WHERE s_id = "+ filename.split('.')[0]+";"
                    mycursor.execute(upp)

mydb.commit()


# [] Add code to make a copy of the folder 
# [] read json 
# [] commit it to mysql

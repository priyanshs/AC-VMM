import os
import shutil
import mysql.connector
import json
import math

# os.system("mkdir grading")
# os.system("mkdir grading/testing")
# os.system("mkdir grading/testing/input")
# os.system("mkdir grading/testing/output")
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mydatabase",
)
mycursor = mydb.cursor()

student_list = []
movdir = "student-code/code/"
basedir = "student-code/grading"
# Walk through all files in the directory that contains the files to copy
for root, dirs, files in os.walk(movdir):
    # print( root, dirs, files )
    for filename in files:
        old_name = os.path.join( os.path.abspath(root), filename )
        stu = root.split('/')[2]    
        file_n = stu + ".py"
        # print(stu)
        student_list.append(stu)
        # Initial new name
        new_name = os.path.join(basedir, file_n)
        shutil.copy(old_name, new_name)


os.system("mkdir student-code/static")
os.system("cp student-code/grading/*.py student-code/static/")
os.system("./student-code/static_checker student-code/static")
os.system("rm -r student-code/static")

relative_plag = {i:0 for i in student_list} 
f = open('results.json')
data = json.load(f)
for i in data['data']:
    file_checking = i['source_name'].split('/')[2].split('.')[0]
    for res in i['checker_result']: 
        curr_score = math.ceil(float(res['similarity_score'])*100)
        comp_to = res['target_name'].split('/')[2].split('.')[0]
        if relative_plag[file_checking] < curr_score : 
            relative_plag[file_checking] = curr_score
        if relative_plag[comp_to] < curr_score: 
            relative_plag[comp_to] = curr_score

for i in relative_plag:
    upp = "UPDATE grading SET static_dist = "+str(relative_plag[i])+" WHERE s_id = "+ i+ ";"
    mycursor.execute(upp)
    
f.close()

basedir = "student-code/grading"
# print(os.path.abspath(basedir))
os.system("autograder run " + os.path.abspath(basedir) + "/ > /dev/null")



student_score = {i:0 for i in student_list}


scorepath = basedir + "/results/"
for root, dirs, files in os.walk(scorepath):
    # print( root, dirs, files )
    for filename in files:
        with open(scorepath + filename, 'r') as fp:
            lines = fp.readlines()
            for row in lines:
                word = 'Result:'
                if row.find(word) != -1:
                    # print(filename)
                    upp = "UPDATE grading SET marks = "+row.split()[1].split('/')[0]+" WHERE s_id = "+ filename.split('.')[0]+";"
                    mycursor.execute(upp)

mydb.commit()


# [] Add code to make a copy of the folder 
# [] read json 
# [] commit it to mysql

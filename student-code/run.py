import os
import shutil
import mysql.connector
import json
import math

assign_id = "1"
max_plag = 20
ulimit_no_of_logins = 10
ulimit_time = ulimit_no_of_logins * 1200

llimit_no_of_logins = 1
llimit_time = llimit_no_of_logins * 300

mydb = mysql.connector.connect(
  host="localhost",
  user="gautam",
  password="password",
  database="App",
)

# {
#     "host":"localhost",
#     "port":"3306",
#     "username":"gautam",
#     "password":"password",
#     "database":"App"
# }

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="",
#   database="mydatabase",
# )

# os.system("mkdir grading")
# os.system("mkdir grading/testing")
# os.system("mkdir grading/testing/input")
# os.system("mkdir grading/testing/output")

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

with open('./submissions', 'w') as fp:
    fp.write('\n'.join(student_list))

os.system("cp ./student-code/pyTime ./student-code/static/")

os.system("./student-code/static/pyTime ")
os.system("rm ./student-code/static/pyTime")
os.system("./student-code/static_checker student-code/static")


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
    # upp = "UPDATE grading SET static_dist = "+str(relative_plag[i])+" WHERE s_id = "+ i+ ";"
    upp = "UPDATE student_activity SET static_dist = "+str(relative_plag[i])+" WHERE entry_no = "+ i+ " AND assignment_id = "+assign_id+";"
    mycursor.execute(upp)
    

f.close()

relative_plag = {i:0 for i in student_list} 
f = open('time')
for line in f:
    student_id, time = line.split(',')
    time = str(int(time)/100000)
    # upp = "UPDATE grading SET grading_time = "+time+" WHERE s_id = "+ student_id + ";"
    upp = "UPDATE student_activity SET grading_time = "+time+" WHERE entry_no = "+ student_id + "AND assignment_id = "+assign_id+";"

    mycursor.execute(upp)
    
f.close()


os.system("rm -r student-code/static")
os.system("rm results.json time submissions")

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
                    # upp = "UPDATE grading SET marks = "+row.split()[1].split('/')[0]+" WHERE s_id = "+ filename.split('.')[0]+";"
                    upp = "UPDATE student_activity SET marks = "+row.split()[1].split('/')[0]+" WHERE entry_no = "+ filename.split('.')[0]+ "AND assignment_id = "+assign_id+";"
                    mycursor.execute(upp)

mydb.commit()



for student in student_list: 
    cheat = "0"
    mycursor.execute("SELECT static_dist, marks FROM student_activity WHERE entry_no = "+ student+ "AND assignment_id = "+assign_id+";")
    # mycursor.execute("SELECT time_vm, no_launches, static_dist, marks FROM grading WHERE s_id = "+ student+ ";")
    x = [i for i in mycursor]
    mycursor.execute("SELECT time from student_activity WHERE entry_no = "+ student+ "AND assignment_id = "+assign_id+" ORDER BY time DESC;")
    y = [i for i in mycursor]
    for i in range(len(y)): 
        if i % 2 : 
            time = time - y[i][0]
        else: 
            time = time + y[i][0]    
    vm_count = len(y)//2 
        
    
    if time < llimit_time: 
        cheat = "1"
    elif time > ulimit_time: 
        cheat = "1"
    elif llimit_time < time/ vm_count < ulimit_time and x[0][0] < max_plag:  
        cheat = "0"
    else: 
        cheat = "1"

    mycursor.execute("UPDATE student_activity SET cheat_label = "+ cheat + " WHERE entry_no = "+ student+  "AND assignment_id = "+assign_id+";")
    # mycursor.execute("UPDATE grading SET cheat_label = "+ cheat + " WHERE s_id = "+ student+ ";")
mydb.commit()
# UPDATE grading SET cheat_label = 1 WHERE s_id = 2
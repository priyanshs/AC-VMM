import os
import shutil

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

# basedir = "student-code/grading"
# print(os.path.abspath(basedir))
# os.system("autograder run " + os.path.abspath(basedir) + "/")
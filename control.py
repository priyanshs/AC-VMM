# This file does the controlling of the whole project segment 

import sys
import os 

grade_path = "student-code/grading"
os.system("autograder run " + os.path.abspath(grade_path) + "/")
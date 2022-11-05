import os 

code_folder = "col732_all@dkstra.cse.iitd.ac.in:/.AC-VMM/student-code/code/"
entryno = input ("Give your entry number here:")
submit_file = input("Which file would you want to submit:")
os.system("mkdir " + entryno)
os.system("cp " + submit_file + "./" + entryno + "/")
os.system("scp -r " + entryno + " " + code_folder)
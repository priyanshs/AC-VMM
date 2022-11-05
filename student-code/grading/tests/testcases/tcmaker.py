"""
Generates test case files for autograder
"""

num = -1

f = open("testcases.txt")

i = 3
for line in f:
    num = int(line.strip())
    code = f"def main():\n\tres = student_submission.reachNumber({num})\n\tif res == {num}:\n\t\tPASS()\n\telse:\n\t\tFAIL()\nmain()"
    new_test_case_file = open(f"test{i}.py", "w")
    new_test_case_file.write(code)
    i += 1
print("Done")



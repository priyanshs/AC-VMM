f = open("out.txt", "r")
file1=f.readlines()
f.close()
f = open("out.txt", "r")
file2=f.readlines()
f.close()
for i in range(len(file1)):
    file1[i]=int(file1[i])
for i in range(len(file2)):
    file2[i]=int(file2[i])
def lcs(pattern_1, pattern_2, len_1, len_2):
    if len_1 == 0 or len_2 == 0:
        return 0
    if pattern_1[len_1 - 1] == pattern_2[len_2 - 1]:
        return 1 + lcs(pattern_1, pattern_2, len_1 - 1, len_2 - 1)
    else :
        return max(lcs(pattern_1, pattern_2, len_1 - 1, len_2), lcs(pattern_1, pattern_2, len_1, len_2 - 1))
print(lcs(file1, file2, len(file1), len(file2)))
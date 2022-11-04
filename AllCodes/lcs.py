def lcs(pattern_1, pattern_2, len_1, len_2):
    if len_1 == 0 or len_2 == 0:
        return 0
    if pattern_1[len_1 - 1] == pattern_2[len_2 - 1]:
        return 1 + lcs(pattern_1, pattern_2, len_1 - 1, len_2 - 1)
    else :
        return max(lcs(pattern_1, pattern_2, len_1 - 1, len_2), lcs(pattern_1, pattern_2, len_1, len_2 - 1))
def longest(file1,file2):
    f = open(file1, "r")
    file1=f.readlines()
    f.close()
    f = open(file2, "r")
    file2=f.readlines()
    f.close()
    for i in range(len(file1)):
        file1[i]=int(file1[i])
    for i in range(len(file2)):
        file2[i]=int(file2[i])
    return(lcs(file1, file2, len(file1), len(file2)))
def judgeAll():
    f = open("submissions", "r")
    file=f.readlines()
    f.close()
    f = open("lcs", "w")
    f.close()
    for i in range(len(file)):
        file[i]=file[i][:-1]
    for i in range(len(file)):
        for j in range(len(file)):
            if(i<j):
                f = open("lcs", "a")
                f.write(file[i]+","+file[j]+","+str(longest(file[i]+".txt",file[j]+".txt")))
                f.write("\n")
                f.close()
judgeAll()
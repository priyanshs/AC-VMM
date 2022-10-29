f = open("sample.txt", "r")
file=f.readlines()
f.close()
values=[]
def valueExtract(raw):
    for i in range(len(raw)):
        cut1=raw[i].find('=')+2
        cut2=len(raw[i])-1
        value=raw[i][cut1:cut2]
        value=value.replace('}','')
        value=value.split(',')
        for j in range(len(value)):
            value[j]=int(value[j])
        values.append(value)
    return values
def adjacentCompare(list1,list2):
    for i in range(len(list1)):
        if(list1[i]!=list2[i]):
            #print(list1[i])
            return list2[i]
def valueChanges(values):
    changes=[]
    for i in range(len(values)-1):
        if(values[i]!=values[i+1]):
            changes.append(adjacentCompare(values[i],values[i+1]))
    return changes
out=valueChanges(valueExtract(file))
f = open("out.txt", "w")
for i in range(len(out)):
    f.write(str(out[i])+"\n")
f.close()
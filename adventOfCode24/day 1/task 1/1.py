import datafile,stripData
data = datafile.exampledata2

list1,list2 = stripData.getData(data)

list1 = sorted(list1)
list2 = sorted(list2)

total = 0

for i in range(len(list1)):
    total+=(abs(list1[i]-list2[i]))

print(total)
import datafile, stripData
list1,list2 = stripData.getData(datafile.data)

dict = {}

for number in list1:
    if number in dict:
        pass

    else:
        dict[number] = 0
        for item in list2:
            if item == number:
                dict[number]+=1;
total = 0
print(dict)
for key in list1:
    total+=key*dict[key]

print(total)
def getData(data):
    list1 = []
    list2 = []
    for line in data.strip().split('\n'):
        col1,col2 = line.split()
        list1.append(int(col1))
        list2.append(int(col2))

    return list1,list2


import datafile
def getData(data = datafile.data):
    parent = []
    for line in data.strip().split('\n'):
        temp = []
        splitdata = line.split()
        for dataval in splitdata:
            temp.append(int(dataval))
        parent.append(temp)
    return parent

data = getData()


count = 0

for row in data:
    
    dif = row[1]-row[0]
    print('')
    
    try:
        nature = dif/abs(dif)
        badcount = 0
        for i in range(1,len(row)):
            dif = row[i]-row[i-1]
            newNat = dif/abs(dif)
            if newNat!=nature:
                badcount+=1                

            elif abs(dif)>3:
                badcount+=1                

        print(row)
        print(badcount)

        if badcount<=1:
            count+=1

    except:
        pass

print(count)    
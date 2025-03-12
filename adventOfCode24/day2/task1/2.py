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

def checkRow(row):
    newRow = row.copy()
    #check if it safe normally if not then check to see if data can be removed
    dif = row[1]-row[0]
    try:
        nature = dif/abs(dif)
        failCount = 0
        for i in range(1,len(row)):
            dif = row[i]-row[i-1]
            newNat = dif/abs(dif)
            if newNat!=nature:
                failCount+=1

            elif abs(dif)>3:
                failCount+=1

        if failCount==0:
            print('returning')
            return 1

    except:
        pass

    print('double checking')
    for item in row:
        failCount = 0
        newRow.remove(item)
        
        #if any of the rows work return 1
        #if a row doesnt work just skip

        dif = row[1]-row[0]
        try:
            nature = dif/abs(dif) 
            for i in range(1,len(newRow)):
                dif = newRow[i]-newRow[i-1]
                newNat= dif/abs(dif)
                if newNat!=nature:
                    failCount+=1

                if abs(dif)>3:
                    failCount+=1

            if failCount==0:
                return 1
                

        except:
            pass

        newRow = row.copy()

    return 0

data = getData()

count = 0
for row in data:
    count += checkRow(row)

print(count)
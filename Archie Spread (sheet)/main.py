import gspread, datetime
from google.oauth2.service_account import Credentials

LIGHTRED1 = {
    'red':0.8784,
    'blue':0.4,
    'green':0.4
}

LIGHTRED2 = {
    'red':0.9176,
    'green':0.6,
    'blue':0.6
}

WHITE = {
    'red':1,
    'green':1,
    'blue':1
}

scopes = [
    'https://www.googleapis.com/auth/spreadsheets'
]

creds = Credentials.from_service_account_file('credentials.json',scopes=scopes)
client = gspread.authorize(creds)

sheet_id = '1LZyDovz3UvO99BcPWJWUP-06KgynzjacJmqFA1DfYmo'
sheet = client.open_by_key(sheet_id)

def rewriteFullyPaid(dataSet):
    mainSheet = sheet.sheet1

    startRow = 3
    endRow = 20
    currentDepsoitedData = []

    currentDate = datetime.date.today()
    current_date_str = currentDate.strftime('%d-%m-%Y')

    for row in range(startRow,endRow+1):
        cell_Values = mainSheet.range(row,15,row,18)
        
        if cell_Values[0].value!='':
            values = getValues(cell_Values)
            temparr = []
            temparr.append(values[0])
            temparr.append(values[1])
            temparr.append(values[2])
            temparr.append(current_date_str)
            currentDepsoitedData.append(temparr)
    
    for values in dataSet:
        temparr = []
        temparr.append(values[0])
        temparr.append(values[1])
        temparr.append(values[2])
        temparr.append(current_date_str)
        currentDepsoitedData.append(temparr)

    print(currentDepsoitedData)

    currentDepsoitedData = sorted(currentDepsoitedData,key=lambda x:x[-1])
    currentDepsoitedData.reverse()

    mainSheet.update(currentDepsoitedData,f'{convertColRowtoA1Format(3,15)}:{convertColRowtoA1Format(len(currentDepsoitedData)+3,18)}')

def getValues(data):
    newList = []
    for element in data:
        newList.append(element.value)
        
    return newList

def convertColRowtoA1Format(row,col):
    col_letter = chr(65 + col - 1)
    return f"{col_letter}{row}"

def reWriteUnDeposited(dataSet,nToBlank):
    mainSheet = sheet.sheet1
    changeCellbg(1,3,7,nToBlank+3,WHITE)

    blank2d = []
    for y in range(nToBlank):
        temparr = []
        for x in range(0,7):
            temparr.append('')
        blank2d.append(temparr)

    cellRange = f'{convertColRowtoA1Format(3,1)}:{convertColRowtoA1Format(nToBlank+2,7)}'
    mainSheet.update(blank2d,cellRange)
    
    cellRange = f'{convertColRowtoA1Format(3,1)}:{convertColRowtoA1Format(len(dataSet)+3,7)}'
    mainSheet.update(dataSet,cellRange)

def rewriteDeposited(dataSet):
    mainSheet = sheet.sheet1

    #get all the current paid for deposits
    startRow = 3
    endRow = 20
    currentDepsoitedData = []

    

    for row in range(startRow,endRow+1):
        cell_Values = mainSheet.range(row,8,row,14)
        
        if cell_Values[0].value!='':
            currentDepsoitedData.append(getValues(cell_Values))

    for data in dataSet:
        currentDepsoitedData.append(data)
    currentDepsoitedData = sorted(currentDepsoitedData,key=lambda x:x[-1])
    currentDepsoitedData.reverse()

    fullyPaid = []
    temparr = []
    for dataSet in currentDepsoitedData:
        if dataSet[4][0].lower() == 'y':
            fullyPaid.append(dataSet)
        else:
            temparr.append(dataSet)

    currentDepsoitedData = temparr

    mainSheet.update(currentDepsoitedData,f'{convertColRowtoA1Format(3,8)}:{convertColRowtoA1Format(len(currentDepsoitedData)+3,14)}')

    rewriteFullyPaid(fullyPaid)

def updateUnDeposited():
    mainSheet = sheet.sheet1


    startCell = convertColRowtoA1Format(3,6)
    endCell = convertColRowtoA1Format(20,6)
    cellRange = f'{startCell}:{endCell}'
    cell_Values = mainSheet.range(cellRange)
    depositedRows = []
    stillUndeposited = []

    currentDate = datetime.date.today()
    current_date_str = currentDate.strftime('%d-%m-%Y')

    for i in range(len(cell_Values)):
        try:
            if cell_Values[i].value != '' and cell_Values[i].value[0].lower() == 'y':

                data = getValues(mainSheet.range(i+3,1,i+3,7))
                data[-1] = current_date_str

                depositedRows.append(data)

            elif cell_Values[i].value !='':
                data = getValues(mainSheet.range(i+3,1,i+3,7))
                stillUndeposited.append(data)
        except:
            break
    
    depositedRows = sorted(depositedRows,key=lambda x:x[-1]) #sorts the data based on the date of when the deposit was payed
    depositedRows.reverse() #flips the data else the list is sorted newest to oldest

    reWriteUnDeposited(stillUndeposited,len(depositedRows)+len(stillUndeposited))

    return depositedRows

def changeCellbg(startCol,startRow,endCol,endRow,colour): #x1,y1 ,x2,y2
    startCell = convertColRowtoA1Format(startRow,startCol)
    endcell = convertColRowtoA1Format(endRow,endCol)
    mainSheet = sheet.sheet1
    mainSheet.format(f'{startCell}:{endcell}',{
    "backgroundColor": {
      "red": colour['red'],
      "green": colour['green'],
      "blue": colour['blue']
    }
    })

def getCurrentDeposited():
    mainSheet = sheet.sheet1

    startRow = 3
    endRow = 20
    currentDeposited = []
    for i in range(startRow,endRow+1):
        startCell = convertColRowtoA1Format(i,8)
        endCell = convertColRowtoA1Format(i,14)
        cellRange = f'{startCell}:{endCell}'
        cell_Values = mainSheet.range(cellRange)

        if cell_Values[0].value == '':
            break
        
        tempList = []
        for cellVal in cell_Values:
            tempList.append(cellVal.value)
        currentDeposited.append(tempList)

    print(currentDeposited)



def startProgram():
    newlyDeposited = updateUnDeposited()
    rewriteDeposited(newlyDeposited)

if __name__ == '__main__':
    startProgram()
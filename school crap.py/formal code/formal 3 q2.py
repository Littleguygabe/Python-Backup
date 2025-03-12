enterNum = False
numList = [2,3,4,5,7,11]


while enterNum == True:
    num = int(input('enter a number'))
    numList.append(num)
    enterAgain = input('do you want to enter another number? (Y/N) ')
    enterAgain = enterAgain.upper()
    if enterAgain == 'N':
        enterNum = False
currentLCM = numList[0]

for i in range (0,len(numList)-1):
    for x in range(1,numList[i+1]+1):
        currentMultiple = currentLCM*x

        if currentMultiple%numList[i+1] == 0:
            LCM = currentMultiple
            currentLCM = LCM
            
            break
print(f'the LCM of is {currentLCM}')

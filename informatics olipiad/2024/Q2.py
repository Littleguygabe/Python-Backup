def E(n):
    return n*2

def O(n):
    return (n*2)-1

def T(n):
    currentLen = 0
    i = 1
    while True:
        currentLen+=i
        if currentLen>=n:
            return i
        i+=1
        
def splitDesc(description):
    for i in range(len(description)):
        if description[i] == ' ':
            return description[:i], int(description[i+1:])

def findInsideBracket(descArr):
    bracketPointer = None
    for index in range(len(descArr)):
        if descArr[index] == '(':
            bracketPointer = index
    if bracketPointer == None:
        bracketPointer = 0
    
    return bracketPointer
        
def evaluateDescription(description):
    descArr = []
    description, ith = splitDesc(description)    
    for character in description:
        descArr.append(character)
    
    while len(descArr)>4:
        bracketPointer = findInsideBracket(descArr)
        descArr[bracketPointer] = combineLists(descArr[bracketPointer+1],descArr[bracketPointer+2],ith)
        for i in range(3):
            del descArr[bracketPointer+1]
            
        print(bracketPointer,descArr)
        
def getVal(char,n):
    if char == 'E':
        return E(n)
    
    elif char == 'O':
        return O(n)
    
    elif char == 'T':
        return T(n)
        
def combineLists(R,L,n):
    insideR = getVal(R,n)
    insideL = getVal(L,insideR)
    outsideR = getVal(R,insideL)
    
    return outsideR
    
#desc = evaluateDescription(str(input(': ')))
description = str(input(': '))
evaluateDescription(description)
print('Gabriel Bridger, Burnley College')
print('#########')

# method to set range for initial
# more efficient method to set initial
# way to read notation
# make sure to remove exception handling in final answer

lists = {}
lists['E'] = []
lists['O'] = []
lists['T'] = []

class stack():
    def __init__(self):
        self.contents = []

    def push(self,x):
        self.contents.append(x)

    def pop(self):
        return self.contents.pop()

def splitInput(string):
    for i in range(len(string)):
        if string[i] == ' ':
            return string[:i], string[i+1:]

def findCenterIndex(desc):
    pointer = 0
    for i in range(len(desc)):
        if desc[i] == '(':
            pointer = i+1 #points to eventual left character
    return pointer

def output(arr,index):
    print(arr[int(i)-1])

def evaluateDesc(desc,index):
    compIndex = findCenterIndex(desc)
    L = lists[desc[compIndex]]
    R = lists[desc[compIndex+1]]
    C = combineLists(L,R)
    output(combineLists(lists[desc[0]],lists[desc[1]]),index)
    
for i in range(1,1001):
    if i%2 == 0:
        lists['E'].append(i)

    else:
        lists['O'].append(i)

    for j in range(i):
        lists['T'].append(i)

def combineLists(L,R):
    C = []
    try:
        for i in range(0,len(R)):
            C.append(R[L[R[i]-1]-1])
 
    except:
        lists['C'] = C
        return C

description, i = splitInput(str(input('Enter Description: ')))

arr = []
for character in description:
    arr.append(character)
evaluateDesc(arr,i)

matrix = [[2,1,3],
          [2,1,2],
          [2,8,2],
          [2,1,2],
          [1,2,2]]    
def findShortest(matrix):
    total = 0
    x = 0
    y = 0
    #find lowest val's x coord in first row
    for i in range(len(matrix[0])):
        if matrix[0][i] == min(matrix[0]):
            x = i
        
    total+=matrix[0][x]
    while y<len(matrix)-1:
        x,y,interval = calcNextRow(x,y,matrix)
        total+=interval
        
    return total
        
def calcNextRow(x,y,matrix):
    minVals = {}
    minVals[matrix[y+1][x]] = x,y+1 #below
    if x-1>=0:
        minVals[matrix[y+1][x-1]] = x-1,y+1 # bottom left
    if x+1<=len(matrix[0])-1:
        minVals[matrix[y+1][x+1]] = x+1,y+1 # bottom right
    
    x,y = minVals[min(minVals)]
    return x,y,min(minVals)
        
print(findShortest(matrix))
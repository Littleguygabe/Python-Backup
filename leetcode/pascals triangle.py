numRows = 5

c = 4
nums = [[1],[1,1]]
while len(nums)<=numRows:
    temp = []
    prevTemp = [1,1]
    print(numRows-c)
    for i in range(0,numRows-c):
        try:
            temp.append(prevTemp[i]+prevTemp[i-1])
        except:
            print(prevTemp)
            temp.append(prevTemp[i-1])
        
    c-=1
    nums.append(temp)
    temp = prevTemp
print(nums)
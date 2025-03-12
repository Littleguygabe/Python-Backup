#find a value in an array with time complexity of O(log n)
import time
start = time.time()

nums = [5,7,7,8,8,10]
target = 10

def findTarget(nums,target):
    notfound = True
    numstemp = nums
    while notfound:
        i = int(len(numstemp)/2)
        if target == numstemp[i]:
            notfound = False
        elif target<numstemp[i]:
            numstemp = numstemp[:i] 
        else:
            numstemp = numstemp[i:]
            
        if len(numstemp) == 1 and notfound:
            return[-1,-1]

    for k in range(i,len(nums)):
        if nums[k] != target:
            return [i,k-1]
            

print(findTarget(nums,target))
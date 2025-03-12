import math
nums = [1,3,5,6]
target = 2

def search(nums,target):
    for i in range(0,len(nums),2):
        #check if they are equal
        if nums[i]!=target and nums[i+1]!=target:
            if nums[i]>target:
                return i
            elif nums[i+1]>target:
                return i + 1
        if nums [i] == target:
            return i+1
        else:
            return i+2
    
print(search(nums,target))
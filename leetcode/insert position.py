nums = [1,3,5,6]
target = 5

def search(nums,target):
    l,r = 0,len(nums)-1

    while l<=r:
        mid = l + (r-l)//2
        if target == nums[mid]:
            return mid
        elif target>nums[mid]:
            l = mid+1
        else:
            r = mid-1
    return l
    
    
print(search(nums,target))
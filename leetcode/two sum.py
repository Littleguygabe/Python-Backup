def solution(nums,target):
    nums = sorted(nums)
    l = 0
    r = len(nums)-1

    while True:     
        val = nums[l]+nums[r]
        if val==target:
            arr=[]
            print(l)
            arr.append(l)
            arr.append(r)
            return arr
    
        elif val<target:
            l+=1
        
        elif val>target:
            r-=1

nums = [2,3,4]
target = 7
print(solution(nums,target))

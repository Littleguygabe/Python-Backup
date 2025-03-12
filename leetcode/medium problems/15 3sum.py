def solution(nums):
    # find all triples that sum 0 -- no duplicates
    res = []
    nums.sort()
    for i,a in enumerate(nums):
        if i>0 and a == nums[i-1]: # if duplicate number skip the iteration as wud create duplicate and make sure that the item isnt the first in the list else it would create an error
            continue

        l,r = i+1,len(nums) -1 #setup pointerd
        while l<r: #ensure that the pointers do not cross
            threesum = a + nums[l]+nums[r] #calculate the current value of the 3 sum
            
            if threesum<0:
                l+=1
            elif threesum>0:
                r-=1
            
            elif threesum == 0:
                res.append([a,nums[l],nums[r]])
                l+=1 #iterate the left pointer as we shift form left to right through the array
                while nums[l] == nums[l-1] and l<r:
                    l+=1 #keep shifting left so long as the left pointer points to the same number until the left pointer hits the right pointer
                         #at which point both for loops break so the next a is used

    return res

nums = [-1,0,1,2,-1,-4]
print(solution(nums))
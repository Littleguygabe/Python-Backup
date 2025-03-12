def solution(height):
    l,r = 0,len(height)-1
    leftMax,rightMax = height[l],height[r]
    
    vol = 0

    while l<r:
        if leftMax>rightMax: #ensure that the pointers dont clash together
            r-=1
            rightMax = max(rightMax,height[r])# by updateing before adding to volume reduces the need to check if it is greater than 0
                                              # as left and right max will never decrease and initially can never be set below 0 due to the structure of the question
                                              # the max will always be greater than 0 hence no need to check that it is greater than 0 or not
            vol+= rightMax-height[r]
        else:
            l+=1
            leftMax = max(leftMax,height[l]) #same as above 
            vol += leftMax-height[l]

    return vol

height = [4,2,3]
print(solution(height))
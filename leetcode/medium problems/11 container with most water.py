def maxArrea(heights):
    l,r = 0,len(heights)-1
    maxVol = 0  
    while l<r:
        vol = min(heights[l],heights[r])*(r-l)
        maxVol = max(vol,maxVol)
        if heights[l]<heights[r]:
            l+=1
        else:
            r-=1
    return maxVol

heights = [2,3,4,5,18,17,6]
print(maxArrea(heights))
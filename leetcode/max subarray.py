nums = [-2,1,-3,4,-1,2,1,-5,4]

ms = 0
cs = 0
for num in nums:
    cs+=num
    if cs<0:
        cs=0
        
    if cs>ms:
        ms=cs
        
return ms


import numpy as np
viewDistance = 2
phValues = np.arange(1,101)
phValues.shape = (10,10)
print(phValues)

xpos = 5
ypos = 4

print(phValues[ypos,xpos])


finalarr = np.zeros((viewDistance*2+1)*(viewDistance*2+1))
finalarr.shape = (viewDistance*2+1,viewDistance*2+1)

for y in range(viewDistance*-1,viewDistance+1):
    temparr = []
    print(y)
    for x in range(viewDistance*-1,viewDistance+1):
        phVal = phValues[ypos+(y),xpos+(x)]
        finalarr[y,x] = phVal

print(finalarr)

import opensimplex
import numpy as np
arr = []
""" x=10
y=10
scaling = 0.1
arr=np.arange(y*x).reshape(x,y)
for y in range(len(arr)):
    for x in range(len(arr[y])):
        arr[y][x] = opensimplex.noise2(x*scaling,y*scaling)
        
print(arr) """
for i in range(0,5):
    temparr = []
    for x in range(0,5):
        
        temparr.append(opensimplex.noise2(i*0.05,x*0.05))
    arr.append(temparr)
    
for i in range(len(arr)):
    print(arr[i])
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

fig,ax = plt.subplots()

def function(xlower,xupper):
    yvals = []
    xvals=[]
    for x in range(xlower,xupper+1):
        y=(x**3)*10
        xvals.append(x)
        yvals.append(y)
    return xvals,yvals


xvals,yvals = function(-5,5)
ax.plot(xvals,yvals)

plt.show()
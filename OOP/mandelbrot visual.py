import numpy as np
import matplotlib.pyplot as plt
import os

def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z)>2:
            return n
        z = z*z + c
    return max_iter

def mandelbrot_set(xmin,xmax,ymin,ymax,width,height,max_iter):
    x = np.linspace(xmin,xmax,width)
    y = np.linspace(ymin,ymax,width)

    mset = np.zeros((height,width))

    for i in range(height):
        for j in range(width):
            c = complex(x[j],y[i])
            #print(f'{round(((i*height+j)/(width*height))*100,3)}%')
            mset[j,i] = mandelbrot(c,max_iter)

    return mset

xmin,xmax,ymin,ymax = -2.0,1.0,-1.5,1.5
width,height = 1000,1000
max_iter = 100
mandelbrot_image = mandelbrot_set(xmin,xmax,ymin,ymax,width,height,max_iter)

plt.imshow(mandelbrot_image,extent = [xmin,xmax,ymin,ymax],cmap='hot')
plt.colorbar()
plt.show()




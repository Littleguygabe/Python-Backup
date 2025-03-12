import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import random,time

class dataPoint():
    def __init__(self,xmax,ymax) -> None:
        self.x=random.randint(0,xmax)
        self.y = random.randint(0,ymax)

        try:
            if self.y/self.x>1:
                self.colour='red'
            elif self.y/self.x<1:
                self.colour = 'blue'
            else:
                self.colour='black'

        except:
            self.colour = 'red'

def startProg():
    xMax = 20
    yMax = 20

    nDataPoints = 100
    fig,ax = plt.subplots()
    data = []
    for i in range(nDataPoints):
        point = dataPoint(xMax,yMax)
        data.append(point)
        plt.scatter(point.x,point.y,c=point.colour)


    plt.show()

if __name__ == '__main__':
    startProg()
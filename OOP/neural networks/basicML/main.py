import matplotlib.pyplot as plt
import random

def plotdata(dataset):
    for data in dataset:
        plt.scatter(data.x,data.y,c=data.colour)

class dataPoint():
    def __init__(self,maxVal):
        self.x = random.randint(0,maxVal)
        self.y = random.randint(0,maxVal)

        if (self.x**2)+(self.y**2)>(maxVal/1.5)**2:
            self.set = 2
            self.colour='#ff0000'
        else:
            self.set = 1
            self.colour='#00ff00'

def learnSet(dataset,maxVal):
    accuracy = 10
    slimmedDataSet = []

    for i in range((int(accuracy/2)),maxVal-((int(accuracy/2))-1),accuracy):
        for data in dataset:
            if x-(int(accuracy/2))<=data.x<=x+(int(accuracy/2)):
                slimmedDataSet.append(data)

    finalisedDataSet = []

    for i in range((int(accuracy/2)),maxVal-((int(accuracy/2))-1),accuracy):
        for data in slimmedDataSet:
            if y-(int(accuracy/2))<=data.y<=y+(int(accuracy/2)):
                data.colour = '#0000ff'
                finalisedDataSet.append(data)            

    plotdata(finalisedDataSet)

def startprogram():
    maxVal = 100
    nPointsOfData = 1000

    dataset=[]
    for i in range(nPointsOfData):
        dataset.append(dataPoint(maxVal))
    
    plotdata(dataset)
    learnSet(dataset,maxVal)

    plt.show()

if __name__ == '__main__':
    startprogram()
import random, math
def createDataSet(nPointsOfData,maxVal):
    dataset1 = []
    dataset2 = []
    for i in range(nPointsOfData):
        temparr=[]
        x=random.randint(0,maxVal)
        y=random.randint(0,maxVal)
        temparr.append(x)
        temparr.append(y)
        if ((x**2)+(y**2))<=5000:
            dataset1.append(temparr)
        else:
            dataset2.append(temparr)

    return dataset1,dataset2
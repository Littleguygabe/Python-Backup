#train a nueral network on the AAPL data, can then try to predcit whether it is going to go up or down in a given day
    #figure out how to parse data in --> input nodes are the closing values of the day before. could have to start further 
    #through in the data for the first section of training, can also train it on other stocks not just AAPL as they will follow 
    #somewhat similar trends so all training data can be used

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class calcSignals():
    def getDEMA(file,N,timeScale): #N is the number of days that the initial SMA (EMA1) is calculated off of,
        #Ndays is how many days it calculates the EMA for 

        closeData = file['Close/Last'].to_numpy()
        
        calcSignals.stripDollar(closeData)
        closeData = np.flipud(closeData) #flip if data in csv is newest to oldest
        closeData = closeData[np.size(closeData)-timeScale:]
        closeData = closeData.astype('f')
        

        EMA = np.zeros(np.size(closeData))
        
        alpha = 2 / (N + 1)
        
        EMA[0] = closeData[0]  
        for i in range(1, np.size(closeData)):
            EMA[i] = (closeData[i] * alpha) + (EMA[i-1] * (1 - alpha))
        

        return EMA,closeData
        
    def getBuyPoints(longEMA,shortEMA):

        
        Buy=False
        for i in range(np.size(shortEMA)):
            if not Buy and longEMA[np.size(longEMA)-np.size(shortEMA)+i]<shortEMA[i]:
                plt.plot(np.size(longEMA)-np.size(shortEMA)+i-1,shortEMA[i-1],'gx')
                Buy = True
            elif Buy and longEMA[np.size(longEMA)-np.size(shortEMA)+i]>shortEMA[i]:
                plt.plot(np.size(longEMA)-np.size(shortEMA)+i-1,shortEMA[i-1],'rx')
                Buy = False


    def stripDollar(dataframe):
        for i in range(len(dataframe)):
            if dataframe[i][0] == '$':
                dataframe[i] = dataframe[i][1:]



def main():
    aapl = pd.read_csv('TSLA.csv')

    longEMA, longCloseData = calcSignals.getDEMA(aapl,100,1000)
    shortEMA, shortCloseData = calcSignals.getDEMA(aapl,10,1000)

    plt.plot(np.arange(0,np.size(longCloseData)),longCloseData,'b-')
    plt.plot(np.arange(0,np.size(longEMA)),longEMA,'r-')
    plt.plot(np.arange(np.size(longEMA)-np.size(shortEMA),np.size(longEMA)),shortEMA,'g-')

    calcSignals.getBuyPoints(longEMA,shortEMA)

    plt.show()

if __name__ == '__main__':
    main()

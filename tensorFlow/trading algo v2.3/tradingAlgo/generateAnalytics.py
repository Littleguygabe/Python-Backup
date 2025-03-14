import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

class debugOptions:
    plotTradeGradients = False
    plotAllBSPoints = False

    plotBuySideAnalytics = False
    plotSellSideAnalytics = False

class thresholdVals:
    lowerBandThresh = 25
    upperBandThresh = 25
    lowerATRThresh = 25 #threshold to classify stock as stable based on atr
    upperATRThresh = 25 #threshold to classify stock as volatile/risky
    highMACDSIGdif = 72


    highRSI = 60
    goodRSI = 50
    lowRSI = 40
    rsiDif = 3 #the threshold of difference in RSI between the current and previous day that means a high or low difference
    highMACDSIGavg = 10 #divide the value by 10 when evalutating -> changes how high the average of the MACD and signal line needs to be in order to constitute a sell point

class weights:
    BBWweight = 1


def colourText(val):
    return val

    if val == 1:
        return f'{GREEN}{val}{RESET}'
    return f'{RED}{val}{RESET}'

def getMAs(rawdf):
    rawdf = rawdf.copy()
    rawdf['SMA10'] = rawdf['Close/Last'].rolling(window=10).mean()
    rawdf['SMA20'] = rawdf['Close/Last'].rolling(window=20).mean()
    rawdf['SMA50'] = rawdf['Close/Last'].rolling(window=50).mean()
    rawdf['10to50SMA'] = np.where(rawdf['SMA10']>rawdf['SMA50'],1,-1)
    

    rawdf['EMA10'] = rawdf['Close/Last'].ewm(span=10,adjust=False).mean()
    rawdf['EMA50'] = rawdf['Close/Last'].ewm(span=50,adjust=False).mean()
    rawdf['EMA12'] = rawdf['Close/Last'].ewm(span=12,adjust=False).mean()
    rawdf['EMA26'] = rawdf['Close/Last'].ewm(span=26,adjust=False).mean()

    rawdf['10to50EMA'] = np.where(rawdf['EMA10']>rawdf['EMA50'],1,-1)

    rawdf['10to50EMA'] = rawdf['10to50EMA'].apply(colourText)
    rawdf['10to50SMA'] = rawdf['10to50SMA'].apply(colourText)
    return rawdf


def getMACDSIG(rawdf):
    rawdf = rawdf.copy()
    rawdf['MACDline'] = rawdf['EMA12'] - rawdf['EMA26']
    rawdf['SigLine'] = rawdf['MACDline'].ewm(span=9,adjust=False).mean()
    rawdf['MACDSIG'] = np.where(rawdf['MACDline']>rawdf['SigLine'],1,-1)

    rawdf['MACDSIG'] = rawdf['MACDSIG'].apply(colourText)
    rawdf['MACDSIGchanged'] = rawdf['MACDSIG']-rawdf['MACDSIG'].shift(1)


    rawdf['normMACDSIGdif'] = min_max_normalize(rawdf['MACDline']-rawdf['SigLine'])*100
    rawdf['normMACDSIGindicator'] = np.where(rawdf['normMACDSIGdif']>thresholdVals.highMACDSIGdif,1,0)
    return rawdf

def getRSI(rawdf):
    rawdf = rawdf.copy()

    rawdf['DailyChange'] = rawdf['Close/Last']-rawdf['Close/Last'].shift(1)
    rawdf['Gain'] = np.maximum(rawdf['DailyChange'],0)
    rawdf['Loss'] = np.maximum(rawdf['DailyChange']*-1,0)

    rawdf['RelStren'] = (rawdf['Gain'].rolling(window=14).mean())/(rawdf['Loss'].rolling(window=14).mean())
    rawdf['RSI'] = 100 - (100/(1+rawdf['RelStren']))
    rawdf['RSIindicator'] = np.where(rawdf['RSI']>thresholdVals.highRSI,2,np.where(rawdf['RSI']>thresholdVals.goodRSI,1,np.where(rawdf['RSI']<thresholdVals.lowRSI,-1,0)))
    rawdf['RSIindicator'] = rawdf['RSIindicator'].apply(colourText)

    ### want to get how the rsi is changing, so want to calculate the difference between todays RSI and yesterdays RSI, then take the EMA of that
    rawdf['RSIprevDif'] = rawdf['RSI']-rawdf['RSI'].shift(1)
    rawdf['RSIdifIndicator'] = np.where(rawdf['RSIprevDif']>thresholdVals.rsiDif,1,0)

    return rawdf

def min_max_normalize(column):
    min_val = column.min()
    max_val = column.max()
    return (column - min_val) / (max_val - min_val)

def getATR(rawdf):
    rawdf = rawdf.copy()
    rawdf['trueRange'] = np.maximum(rawdf['High']-rawdf['Low'],np.maximum((rawdf['High']-(rawdf['Close/Last'].shift(1))).abs(),(rawdf['Low']-(rawdf['Close/Last'].shift(1))).abs()))
    rawdf['ATR'] = rawdf['trueRange'].rolling(window=14).mean()
    rawdf['ATR'] = min_max_normalize(rawdf['ATR'])*100
    rawdf['ATRindicator'] = np.where(rawdf['ATR'] < thresholdVals.lowerATRThresh, 0,
                          np.where(rawdf['ATR'] > (100 - thresholdVals.upperATRThresh), 2, 1))

    return rawdf

def getBB(rawdf):
    rawdf = rawdf.copy()

    rawdf['middleBand'] = rawdf['SMA20']
    rawdf['stdDev'] = rawdf['Close/Last'].rolling(window=20).std()
    rawdf['upperBand'] = rawdf['middleBand']+2*rawdf['stdDev']
    rawdf['lowerBand'] = rawdf['middleBand']-2*rawdf['stdDev']

    #how close the close is to the lower band -> difference between close and low band value as a percentage of the band width
    rawdf['LBClsPctDif'] = (rawdf['Close/Last']-rawdf['lowerBand'])/(rawdf['upperBand']-rawdf['lowerBand'])*100

    rawdf['BBWClsPctDifIndicator'] = np.where(rawdf['LBClsPctDif']<thresholdVals.lowerBandThresh,1,np.where(rawdf['LBClsPctDif']>(100-thresholdVals.upperBandThresh),2,0))
    rawdf['BBWClsPctDifIndicator'] = rawdf['BBWClsPctDifIndicator'].apply(colourText) 

    return rawdf

def getOBV(rawdf):
    rawdf = rawdf.copy()
    rawdf['OBV'] = 0  # Initialize OBV column
    
    # Iterate over the DataFrame from the bottom to the top
    for i in range(1, len(rawdf)):  # Start from 1 because OBV[0] is initialized as 0
        if rawdf['Close/Last'][i] > rawdf['Close/Last'][i - 1]:  # Price increased
            rawdf.loc[i, 'OBV'] = rawdf.loc[i - 1, 'OBV'] + rawdf.loc[i, 'Volume']
        elif rawdf['Close/Last'][i] < rawdf['Close/Last'][i - 1]:  # Price decreased
            rawdf.loc[i, 'OBV'] = rawdf.loc[i - 1, 'OBV'] - rawdf.loc[i, 'Volume']
        else:  # Price stayed the same
            rawdf.loc[i, 'OBV'] = rawdf.loc[i - 1, 'OBV']

    rawdf['normalisedOBV'] = min_max_normalize(rawdf['OBV'])
    rawdf['normalisedOBV']*=100
    #rawdf['normOBVSMA100'] = rawdf['normalisedOBV'].rolling(window=10).mean()
    rawdf['normOBVSMA100'] = rawdf['normalisedOBV'].ewm(span=25,adjust=False).mean()

    rawdf['normOBVSMAindicator'] = np.where(rawdf['normalisedOBV']>rawdf['normOBVSMA100'],1,-1)

    rawdf['buyingPressureIndicator'] = np.where(rawdf['OBV']>0,1,-1)
    rawdf['buyingPressureIndicator'] = rawdf['buyingPressureIndicator'].apply(colourText)


    return rawdf


def plotBands(rawdf):
    ####
    #Every time the price hits the top bollinger band almost instantly afterwards it corrects and the value drops
    ####
    plt.plot(rawdf.index,rawdf['Close/Last'],label='Price')
    plt.plot(rawdf.index,rawdf['middleBand'],label='middle')
    plt.plot(rawdf.index,rawdf['upperBand'],label='upper')
    plt.plot(rawdf.index,rawdf['lowerBand'],label='lower')
    plt.plot(rawdf.index,rawdf['LBClsPctDif'],label='LBClsPctDif')

    plt.legend()
    plt.grid(True)
    plt.show()

class buySellPoints():
    def __init__(self,rawdf):
        self.rawdf = rawdf
        self.points = []

    def addBuyPoint(self,index):
        self.points.append(['Buy',float(self.rawdf.loc[index,'Close/Last']),index])

    def addSellPoint(self,index):
        self.points.append(['Sell',float(self.rawdf.loc[index,'Close/Last']),index])

    def print(self):
        print(self.points)        

    def shouldBuyStock(self,i):
        curSeries = self.rawdf.loc[i]
        #if curSeries['BBWClsPctDifIndicator'] == 1 and curSeries['RSIindicator']>=1 and curSeries['normOBVSMAindicator']==-1: #weirdly has generated good points for exit not entry
        if (curSeries['RSIindicator']==-1
            and curSeries['BBWClsPctDifIndicator'] == 1
            and curSeries['normOBVSMAindicator'] == -1):
        ### basically want to be able to identify the where every trough is -> once can do that then good

            return True


        return False

    def shouldSellStock(self,i):
        curSeries = self.rawdf.loc[i]
        #if curSeries['BBWClsPctDifIndicator'] == 2 and curSeries['SMA10']>curSeries['EMA10'] and curSeries['MACDSIG']>0 and curSeries['RSIindicator'] <2:
        if (curSeries['RSIdifIndicator']==1 and curSeries['EMA10']>curSeries['SMA10'] and (curSeries['MACDline']+curSeries['SigLine'])/2>(thresholdVals.highMACDSIGavg/10)
            and curSeries['RSIindicator'] > 1
            and curSeries['normMACDSIGindicator']==1 ):
            return True

        return False 

    def generatePoints(self):
        for i in range(len(self.rawdf)):
            if self.shouldBuyStock(i):
                self.addBuyPoint(i)

            elif self.shouldSellStock(i):
                self.addSellPoint(i)


        #### ^^^ all the logic to control the buying algorithms

        return self.plotPagainstPrice()

    def plotPagainstPrice(self):


        plt.plot(self.rawdf.index,self.rawdf['Close/Last'],label='Price')
        self.buyIndexes = []
        self.buyPrices = []

        self.sellIndexes = []
        self.sellPrices = []

        for i in range(len(self.points)):
            curPoint = self.points[i]
            if curPoint[0]=='Buy':

                self.buyIndexes.append(curPoint[2])
                self.buyPrices.append(curPoint[1])

            elif curPoint[0]=='Sell':
                self.sellIndexes.append(curPoint[2])
                self.sellPrices.append(curPoint[1])            

        if debugOptions.plotAllBSPoints:
            self.plotDataFromPL()

        profitEvaluator = profitEval(self.points,self.rawdf)
        return profitEvaluator.zipBuySell()

       

    def plotDataFromPL(self):

        plt.scatter(self.buyIndexes,self.buyPrices,label = 'Buy Marker',marker = 'x',color = 'green') 
        plt.scatter(self.sellIndexes,self.sellPrices,label = 'Sell Marker',marker = 'x',color = 'red') 

        if debugOptions.plotSellSideAnalytics:           
            plt.plot(self.rawdf.index,self.rawdf['RSIprevDif'],label = 'RSI prev dif',color='purple',alpha=0.5)
            plt.plot(self.rawdf.index,self.rawdf['SMA10'],label = 'sma10',color='black',alpha=1)               
            plt.plot(self.rawdf.index,self.rawdf['EMA10'],label = 'EMA10',color='red')       
            plt.plot(self.rawdf.index,((self.rawdf['MACDline']+self.rawdf['SigLine'])/2)*10,label = 'MACD SIG average',color = 'pink')
            plt.plot(self.rawdf.index,self.rawdf['normMACDSIGdif'],label = 'normMACDSIGdif',color = 'orange')


            plt.axhline(y=thresholdVals.rsiDif,linestyle='--',color='purple',label='rsi dif threshold')
            plt.axhline(y=thresholdVals.highMACDSIGavg,linestyle = '--',color='pink',label='macdSig avg')
            plt.axhline(y=thresholdVals.highMACDSIGdif,linestyle='--',color='orange',label = 'high macd sig dif threshold')





        if debugOptions.plotBuySideAnalytics:
            plt.plot(self.rawdf.index,self.rawdf['MACDline']*10,label='MACD*10')
            plt.plot(self.rawdf.index,self.rawdf['SigLine']*10,label='Sig line * 10')
            plt.plot(self.rawdf.index,self.rawdf['normMACDSIGdif'],label = 'normalised dif between macd and sig')

            plt.plot(self.rawdf.index,self.rawdf['LBClsPctDif'],label = 'LBClsPctDif',alpha=0.5)
            plt.plot(self.rawdf.index,self.rawdf['upperBand'],label='upper')
            plt.plot(self.rawdf.index,self.rawdf['lowerBand'],label='lower')
            plt.axhline(thresholdVals.highMACDSIGdif,linestyle = '--',label = 'high macd sig dif threshold')  
        
        plt.grid(True)
        
        plt.legend()
        plt.show()

class profitEval():
    def __init__(self,points,rawdf):
        self.points = points
        self.rawdf = rawdf

    def zipBuySell(self):
        sortedPoints = self.quickSortPoints(self.points)
        strippedPoints = self.getSingleBuyToSellPoints(sortedPoints)
        sumOfIncreases = 0

        for i in range(0,len(strippedPoints)-1,2):
            sumOfIncreases+= round(strippedPoints[i+1][1]/strippedPoints[i][1],3)
        print(f'average increase per investment ->\t{sumOfIncreases/(len(strippedPoints)/2)} \t{self.rawdf.loc[0,'symbol']}')

        if debugOptions.plotTradeGradients:
            self.plotBuyToSellPoints(strippedPoints)

        return sumOfIncreases/(len(strippedPoints)/2)

    def plotBuyToSellPoints(self,strippedPoints):

        plt.plot(self.rawdf.index,self.rawdf['Close/Last'],label = 'Price')
        for i in range(0,len(strippedPoints)-1,2):
            plt.plot([strippedPoints[i][2],strippedPoints[i+1][2]],[strippedPoints[i][1],strippedPoints[i+1][1]],color='red')




        plt.legend()
        plt.grid(True)
        plt.show()

    def getSingleBuyToSellPoints(self,sortedPoints):
        bs = 0
        strippedPoints = []
        for i in range(len(sortedPoints)-1):
            if bs%2 == 0 and sortedPoints[i][0]=='Buy':
                strippedPoints.append(sortedPoints[i])
                bs+=1

            elif bs%2 == 1 and sortedPoints[i][0]=='Sell':
                strippedPoints.append(sortedPoints[i])
                bs+=1

        return strippedPoints

    def quickSortPoints(self,arr):
        less = []
        greater = []
        equal = []

        if len(arr)>1:
            pivot = arr[0][2]
            for x in arr:
                if x[2]<pivot:
                    less.append(x)
                elif x[2]>pivot:
                    greater.append(x)
                else:
                    equal.append(x)

            return self.quickSortPoints(less)+equal+self.quickSortPoints(greater)
        
        else:
            return arr


def splitIndicatorsMetrics(rawdf):
    indicatorCols = ['10to50SMA','10to50EMA','MACDSIG','RSIindicator','ATRindicator','BBWClsPctDifIndicator','buyingPressureIndicator','RSIdifIndicator']

    indicatorsDf = rawdf[indicatorCols]
    metricsDf = rawdf.drop(columns=indicatorCols)

    return indicatorsDf,metricsDf

def getAnalyticDf(rawdf):
    rawdf.reset_index(drop=True,inplace=True)
    rawdf = getMAs(rawdf)
    rawdf = getMACDSIG(rawdf)
    rawdf = getRSI(rawdf)
    rawdf = getATR(rawdf)
    rawdf = getBB(rawdf)
    rawdf = getOBV(rawdf)
    #plotBands(rawdf)

    bsp = buySellPoints(rawdf)
    averageValuation = bsp.generatePoints()

    indicators,metrics = splitIndicatorsMetrics(rawdf)


    """colnames = rawdf.columns.tolist()
    for col in colnames:
        print(col)

    print(indicators)
    print(metrics) """

    return indicators,averageValuation


def main(rawdf):
    rawdf,avgVal = getAnalyticDf(rawdf)
    
    return rawdf,avgVal

if __name__ == '__main__':
    stockIndxs = []
    avgReturn = []

    fileList = os.listdir('nasdaq100')
    for i in range(len(fileList)):
        testRawdf = pd.read_csv(f'nasdaq100/{fileList[i]}')
        testOutputDF,avgVal = main(testRawdf[::-1])
        if avgVal!=0:
            stockIndxs.append(i)
            avgReturn.append(avgVal-1)
    
    
    #plt.scatter(stockIndxs,avgReturn)
    #plt.show()
    avgIncrease = round((sum(avgReturn)/len(avgReturn))-1,3)
    if avgIncrease>0:
        print(f'Global Average Return -> \t+{avgIncrease*100}%')

    else:
        print(f'Global Average Return -> \t-{avgIncrease*100}%')

    


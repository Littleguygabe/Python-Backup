import analyticDataFrameCreationFiles.generateVolatilityAnalytics as gva
import analyticDataFrameCreationFiles.generateMomentumAnalytics as gma
import pandas as pd
import os
import time
import marketSim as ms

from sklearn.cluster import KMeans

import matplotlib.pyplot as plt

maxPurchaseVal = 1000

stocksToPredictFolderName = 'backtestingData'

def getTickers():
    fileList = os.listdir(stocksToPredictFolderName)
    tickers = []
    for item in fileList:
        fileName,extension = os.path.splitext(item)
        tickers.append(fileName)

    return tickers

def zipInSymbols(df):
    tickers = getTickers()

       
    df.reset_index(drop=True)    

    try:
        df['symbol'] = tickers
    except:
        print(tickers)
        time.sleep(5)
    
    return df

def sortDfListOnMostRecentBBWATR(dfList):
    newdf = pd.DataFrame()


    for df in dfList:
        if newdf.empty:
            newdf = pd.DataFrame(columns=df.columns)  # Ensure correct structure
        newdf = pd.concat([newdf,df.head(1)],axis=0)

    newdf = gva.sortHighBBWLowATR(newdf)

    return newdf

def stripUnNeededRowsForVolatility(sortedCombinedAnalyticsDf):
    newdataFrame = sortedCombinedAnalyticsDf[['symbol','BBWATRmetric']].copy()

    return newdataFrame
def sortDfListOnMostRecentVOLCS(momentumdfList):
    newdf = pd.DataFrame()
    for df in momentumdfList:
        newdf = pd.concat([newdf,df.head(1)],axis=0)

    newdf['symbol'] = getTickers()

    newdf = newdf.sort_values(by='volCsMetric',ascending=False)
    return newdf

def stripUnNeedeRowsForVolatility(sortedCombinedMomentumDf):
    newDataFrame = sortedCombinedMomentumDf[['symbol','volCsMetric']].copy()
    return newDataFrame

def getStocksToBuy(df):
    NoStocks = int(len(df)*1)
    stockToBuydf = df.head(NoStocks)
    return stockToBuydf


def purchaseStocks(df,date,portfolio):
    df = df.dropna()
    for i in range(len(df)):
        stock=df.iloc[i]
        portfolio.buyStock(stock.symbol,str(date.values[0]),5000)
        portfolio.printPortfolio()


def getFinalMetricDataFrame():
    VolatiltiydfList = gva.createAnalyticDataFrame(stocksToPredictFolderName)

    print(VolatiltiydfList)

    sortedCombinedAnalyticsDf = sortDfListOnMostRecentBBWATR(VolatiltiydfList)
    strippedCombinedVolatilityAnalyticsDf = stripUnNeededRowsForVolatility(sortedCombinedAnalyticsDf)



    momentumdfList = gma.getMomentumAnalytics(stocksToPredictFolderName)
    sortedCombinedMomentumDf = sortDfListOnMostRecentVOLCS(momentumdfList)
    strippedCombinedMomentumAnalyticsDf = stripUnNeedeRowsForVolatility(sortedCombinedMomentumDf)

    mergedDataFrame = strippedCombinedVolatilityAnalyticsDf.merge(strippedCombinedMomentumAnalyticsDf,on='symbol')

    mergedDataFrame['CombinedMetric'] = mergedDataFrame['BBWATRmetric']*mergedDataFrame['volCsMetric']
    mergedDataFrame = mergedDataFrame.sort_values(by='CombinedMetric',ascending=False)

    return mergedDataFrame

def main(args):
    if len(args)==0:
        myportfolio = ms.Portfolio()
    else:
        myportfolio = args[0]


    mergedDataFrame = getFinalMetricDataFrame()
    print(mergedDataFrame)

    """ plt.scatter(mergedDataFrame['BBWATRmetric'],mergedDataFrame['volCsMetric'],marker='o')
    plt.xlabel('BBWATR')
    plt.ylabel('volCs')
    print('Merged data frame:') """

    stocksToBuy = getStocksToBuy(mergedDataFrame)
    
    """ print('stocks to buy:')
    print(stocksToBuy)"""

    date = pd.read_csv(f'{stocksToPredictFolderName}/{os.listdir(stocksToPredictFolderName)[0]}').head(1)['Date']
        
        
    purchaseStocks(stocksToBuy,date,myportfolio)

    print('Bought Another Round of Stocks')
    myportfolio.printPortfolio()

    #plt.show()
 # creates a data frame of stocks to buy based off of the metric created from analysis of current trend strength -> need to combine with momentum indicators to 
#be able to see which ones have upwards momentum -> create a momentum metric -> decreasing val = -ve increasing val = +ve
#multiple the trend metric with the momentum metric to create a final metric that takes into account trend and momentum 
# -> means that stable stocks with large increasing momentum will be at the top of the data file
# -> could also map the momentum and trend strength values in scatter to cluster/analyse 
### the values just need the most recent stock data

if __name__ == '__main__':
    main()

## need to make sure that symbol is kept through out the process
# iterate over the list of data frames wihtin this file and just pass single data frame to the analytic files
import os
import pandas as pd
import time


import tradingAlgo.genMomentumAnalytics as gma
import tradingAlgo.genVolatitlityAnalytics as gva
import marketSim as ms

import matplotlib as plt
import matplotlib.animation as animation

timings = True

def getfiles(foldername):
    files = os.listdir(f'{foldername}')
    return files

def getRawDataFrames(foldername):
    rawdfList = []
    fileList = getfiles(foldername)
    for file in fileList:
        df = pd.read_csv(f'{foldername}/{file}')
        rawdfList.append(df)

    return rawdfList


def finaliseAnalaytics(volatilityAnalyticsDf,momentumAnalyticsDf):
    mergedDf = pd.merge(volatilityAnalyticsDf,momentumAnalyticsDf,on='symbol')

def getTopStocks(foldername):
    rawDfList = getRawDataFrames(foldername)
    allMostRecentMomAnalytics = pd.DataFrame()
    allMostRecentVolAnalytics = pd.DataFrame()



    for df in rawDfList:
        ## flip data frame so newest is at the bottom, oldest is at the top
        df = df.iloc[::-1].reset_index(drop=True)
        volatilityAnalyticsDf = gva.main(df)
        momentumAnalyticsDf = gma.main(df)
        
        allMostRecentMomAnalytics = allMostRecentMomAnalytics.dropna()
        allMostRecentVolAnalytics = allMostRecentVolAnalytics.dropna()

        volatilityAnalyticsDf = volatilityAnalyticsDf.dropna()
        momentumAnalyticsDf = momentumAnalyticsDf.dropna()
        
    # Check if the DataFrame is not empty and doesn't contain only NaN values
        if not momentumAnalyticsDf.dropna(how='all').empty:
            allMostRecentMomAnalytics = pd.concat([allMostRecentMomAnalytics, momentumAnalyticsDf.tail(1)])

        if not volatilityAnalyticsDf.dropna(how='all').empty:
            allMostRecentVolAnalytics = pd.concat([allMostRecentVolAnalytics, volatilityAnalyticsDf.tail(1)])
      

    allMostRecentMomAnalytics.reset_index(drop=True,inplace=True)
    allMostRecentVolAnalytics.reset_index(drop=True,inplace=True)

    mergedDf = pd.merge(allMostRecentMomAnalytics,allMostRecentVolAnalytics,on='symbol')    
    
    mergedDf['combinedMetric'] = mergedDf['volCsMetric']*mergedDf['BBWATRmetric']


    stocksToBuy = mergedDf[mergedDf['combinedMetric']>0][['symbol','combinedMetric']]
    stocksToBuy = stocksToBuy.sort_values(by='combinedMetric',ascending=False)
    stocksToBuy.reset_index(drop=True,inplace=True)

    stocksToSell = mergedDf[mergedDf['combinedMetric']<10][['symbol','combinedMetric']]
    stocksToSell = stocksToSell.sort_values(by='combinedMetric')
    stocksToSell.reset_index(drop=True,inplace=True)

    return stocksToBuy,stocksToSell

def purchaseStocks(topStocks, portfolio):
    # Normalize the combined metric
    min_val = topStocks['combinedMetric'].min()
    max_val = topStocks['combinedMetric'].max()
    topStocks['normalisedVal'] = (topStocks['combinedMetric'] - min_val) / (max_val - min_val)

    # Create a list of stocks that are currently owned
    stockList = topStocks['symbol'].to_list()
    currentlyOwnedPo = portfolio.ownedStocks
    currentlyOwned = [po.symbol for po in currentlyOwnedPo]

    # Purchase stocks not owned yet
    for stock in stockList:
        if stock not in currentlyOwned:
            # Get the normalized value for the stock
            normalisedValue = topStocks[topStocks['symbol'] == stock]['normalisedVal'].values[0]
            
            # Calculate how much to buy based on the normalised value
            amountToBuy = normalisedValue * 5000  # You can adjust the multiplier as needed
            
            # Buy the stock
            portfolio.buyStock(stock, 1000)


def sellStocks(bottomStocks,portfolio):
    stockList = bottomStocks['symbol'].to_list()
    currentlyOwnedPo = portfolio.ownedStocks
    currentlyOwned = []
    for po in currentlyOwnedPo:
        currentlyOwned.append(po.symbol)

    for stock in stockList:
        if stock in currentlyOwned:
            portfolio.sellStock(stock)


def main(myPortfolio):

    foldername = 'backtestingData'
    if timings:
        tbStart = time.time()
    topStocksdf,badPerformers = getTopStocks(foldername)
    if timings:
        print(f'retrieved stocks in: \t{round(time.time()-tbStart,3)}s\t|')
    
    if timings:
        purchaseStart = time.time()
    purchaseStocks(topStocksdf,myPortfolio)
    if timings:
        print(f'purchased stocks in: \t{round(time.time()-purchaseStart,3)}s\t|')

    if timings:
        sellStart = time.time()
    sellStocks(badPerformers,myPortfolio)
    
    if timings:
        print(f'sold stocks in: \t{round(time.time()-sellStart,3)}s\t|')


if __name__ == '__main__':
    main('backtestingData')

#could maybe create a condition for if all the stocks/portfolio has decreased by a certain value then just sell no matter what -> can help avoid falling into ditches
    #could also result in the algo shorting stocks

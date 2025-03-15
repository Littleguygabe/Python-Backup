import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

class thresholdVals:
    lowerBandThresh = 25
    upperBandThresh = 25
    lowerATRThresh = 25 #threshold to classify stock as stable based on atr
    upperATRThresh = 25 #threshold to classify stock as volatile/risky
    highMACDSIGdif = 72

    peakGradient = -1 #the gradient for 'peakLength' No days after a given point must be less than this to classify as a peak
        #decreasing gradient threshold and decreasing peak length will get a larger number of short sharp peaks
    peakLength = 3

    highRSI = 60
    goodRSI = 50
    lowRSI = 40
    rsiDif = 3 #the threshold of difference in RSI between the current and previous day that means a high or low difference
    highMACDSIGavg = 10 #divide the value by 10 when evalutating -> changes how high the average of the MACD and signal line needs to be in order to constitute a sell point

class weights:
    BBWweight = 1


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

    return rawdf


def getMACDSIG(rawdf):
    rawdf = rawdf.copy()
    rawdf['MACDline'] = rawdf['EMA12'] - rawdf['EMA26']
    rawdf['SigLine'] = rawdf['MACDline'].ewm(span=9,adjust=False).mean()
    rawdf['MACDSIG'] = np.where(rawdf['MACDline']>rawdf['SigLine'],1,-1)

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
    #rawdf['normOBVEMA25'] = rawdf['normalisedOBV'].rolling(window=10).mean()
    rawdf['normOBVEMA25'] = rawdf['normalisedOBV'].ewm(span=25,adjust=False).mean()

    rawdf['normOBVSMAindicator'] = np.where(rawdf['normalisedOBV']>rawdf['normOBVEMA25'],1,-1)

    rawdf['buyingPressureIndicator'] = np.where(rawdf['OBV']>0,1,-1)

    return rawdf

def getPeaks(rawdf):    
    ## look at the gradient of change for the N days after a point to classify as a peak

    rawdf['futureNDayPriceGradient'] = rawdf['DailyChange'].shift((thresholdVals.peakLength-1)*-1).rolling(window=thresholdVals.peakLength).mean() 
    
    rawdf['isPeakIndicator'] = np.where(rawdf['futureNDayPriceGradient']<thresholdVals.peakGradient,1,0)



    return rawdf

def splitIndicatorsMetrics(rawdf):
    indicatorCols = ['Date','Close/Last','10to50SMA','10to50EMA','MACDSIG','MACDSIGchanged','normMACDSIGindicator','RSIindicator','RSIdifIndicator','ATRindicator','BBWClsPctDifIndicator','normOBVSMAindicator','buyingPressureIndicator','isPeakIndicator']

    indicatorsDf = rawdf[indicatorCols]
    metricsDf = rawdf.drop(columns=indicatorCols)

    return indicatorsDf,metricsDf

def getAnalyticDf(rawdf):
    generatingTrainingData = True


    rawdf.reset_index(drop=True,inplace=True)
    rawdf = getMAs(rawdf)
    rawdf = getMACDSIG(rawdf)
    rawdf = getRSI(rawdf)
    rawdf = getATR(rawdf)
    rawdf = getBB(rawdf)
    rawdf = getOBV(rawdf)
    
    if generatingTrainingData:
        rawdf = getPeaks(rawdf)



    indicators,metrics = splitIndicatorsMetrics(rawdf)


    return indicators


def main(rawdf):
    rawdf = getAnalyticDf(rawdf)
    
    return rawdf

if __name__ == '__main__':

    fileList = os.listdir('nasdaq100')
    for i in range(len(fileList)):
        testRawdf = pd.read_csv(f'nasdaq100/{fileList[i]}')
        indicators= main(testRawdf[::-1])
        
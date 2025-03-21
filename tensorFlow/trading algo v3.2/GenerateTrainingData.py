import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import thresholdVals
import sys

### figure out which data values need normalising and normalise them
### use scatter graphs to plot a rough category of data against price (price Y axis, technical analytic X axis) -> could allow for classification???




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
    return rawdf

def getRSI(rawdf):
    rawdf = rawdf.copy()

    rawdf['DailyChange'] = rawdf['Close/Last']-rawdf['Close/Last'].shift(1)
    rawdf['Gain'] = np.maximum(rawdf['DailyChange'],0)
    rawdf['Loss'] = np.maximum(rawdf['DailyChange']*-1,0)

    rawdf['RelStren'] = (rawdf['Gain'].rolling(window=14).mean())/(rawdf['Loss'].rolling(window=14).mean())
    rawdf['RSI'] = 100 - (100/(1+rawdf['RelStren']))
    ### want to get how the rsi is changing, so want to calculate the difference between todays RSI and yesterdays RSI, then take the EMA of that
    rawdf['RSIprevDif'] = rawdf['RSI']-rawdf['RSI'].shift(1)
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
    return rawdf

def getBB(rawdf):
    rawdf = rawdf.copy()

    rawdf['middleBand'] = rawdf['SMA20']
    rawdf['stdDev'] = rawdf['Close/Last'].rolling(window=20).std()
    rawdf['upperBand'] = rawdf['middleBand']+2*rawdf['stdDev']
    rawdf['lowerBand'] = rawdf['middleBand']-2*rawdf['stdDev']

    #how close the close is to the lower band -> difference between close and low band value as a percentage of the band width
    rawdf['LBClsPctDif'] = (rawdf['Close/Last']-rawdf['lowerBand'])/(rawdf['upperBand']-rawdf['lowerBand'])*100

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

    return rawdf

def getEntryExitPoints(rawdf):    
    ## look at the gradient of change for the N days after a point to classify as a peak

    rawdf['futureNDayPriceGradientPeak'] = rawdf['DailyChange'].shift((thresholdVals.peakLength-1)*-1).rolling(window=thresholdVals.peakLength).mean() 
    rawdf['prevNDayPriceGradientPeak'] = rawdf['DailyChange'].rolling(window=thresholdVals.prePeakLength).mean()


    rawdf['futureNDayPriceGradientTrough'] = rawdf['DailyChange'].shift((thresholdVals.troughLength-1)*-1).rolling(window=thresholdVals.troughLength).mean()
    rawdf['prevNDayPriceGradientTrough'] = rawdf['DailyChange'].rolling(window=thresholdVals.preTroughLength).mean()


    rawdf['isPeakIndicator'] = np.where((rawdf['futureNDayPriceGradientPeak']<thresholdVals.postPeakGradient)
                                        & (rawdf['prevNDayPriceGradientPeak']>thresholdVals.prePeakGradient)
                                        ,2, np.where((rawdf['futureNDayPriceGradientTrough']>thresholdVals.postTroughGradient)
                                                    &(rawdf['prevNDayPriceGradientTrough']<thresholdVals.preTroughGradient)
                                                    ,1,0)
                                        )
    return rawdf

def normaliseDF(rawdf):
    columns = rawdf.columns
    for col in columns:
        rawdf[col] = min_max_normalize(rawdf[col])

    return rawdf

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
        rawdf = getEntryExitPoints(rawdf)
        rawdf = rawdf.dropna()
        #rawdf = normaliseDF(rawdf.drop(columns=['symbol','Date']))
        #print(rawdf.columns)


    #plotEntryExitPoints(rawdf)
    return rawdf
 
def main(rawdf):
    rawdf = getAnalyticDf(rawdf)
    
    return rawdf


def saveDataframe(df):
    saveFolder = 'analysisFiles'
    maxFileSize = 100 #max file size in MB

    for file in os.listdir(saveFolder):
        os.remove(f'{saveFolder}/{file}')

    loading_bar(8,1)
    
    df.to_csv(f'{saveFolder}/temp.csv')
    loading_bar(8,2)
    fileSizeMB = os.path.getsize(f'{saveFolder}/temp.csv')/(1024**2)
    loading_bar(8,3)
    os.remove(f'{saveFolder}/temp.csv')
    loading_bar(8,5)


    fileCount = 1
    while fileSizeMB>maxFileSize:
        fileSizeMB/=2
        fileCount*=2

    loading_bar(8,6)

    splitDfLen = len(df)//fileCount
    for i in range(fileCount-1):
        df[splitDfLen*i:splitDfLen*(i+1)].to_csv(f'{saveFolder}/{i+1}.csv',index=False)

    loading_bar(8,7)

    df[splitDfLen*(fileCount-1):].to_csv(f'{saveFolder}/{fileCount}.csv',index=False)

    loading_bar(8,8)
    print()

def loading_bar(total_steps, i, bar_length=40):

    percent = (i / total_steps) * 100
    hashes = '#' * int(i * bar_length / total_steps)
    spaces = ' ' * (bar_length - len(hashes))
    
    sys.stdout.write(f'\r[{hashes}{spaces}] {percent:.2f}%')
    sys.stdout.flush() 



       
def createTrainingDataFile():
    fileList = os.listdir('nasdaq100')

    finalDf = pd.DataFrame()

    for i in range(len(fileList)):
        testRawdf = pd.read_csv(f'nasdaq100/{fileList[i]}')
        rawdf = main(testRawdf[::-1])
        finalDf = pd.concat([finalDf,rawdf])
        loading_bar(len(fileList),i)

    print()

    finalDf = finalDf.reset_index(drop=True,inplace=False)

    saveDataframe(finalDf)
    print('Data Saved Successfully')

if __name__ == '__main__':
    testing = False
    if not testing:
        createTrainingDataFile()

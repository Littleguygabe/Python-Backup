import pandas as pd
import numpy as np

def checkDailyValuation(df):
    df['ValInc'] = np.where(df['Close/Last'] > df['Open'], 1, 0)

def convertColsToFloat(df):
    priceCols = ['Close/Last', 'Open', 'High', 'Low']
    for col in priceCols:
        df[col] = df[col].astype(float)
    return df

def stripDollarSign(df):
    df = df.replace(r'[\$,]', '', regex=True)
    return df

class emaCol:
    def nDayEma(df, n):
        return df['Close/Last'].ewm(span=n, adjust=False).mean()

    def subtractListValues(list1, list2):
        return list1 - list2

    def createShortTermMACDcolumn(df, newdf):
        newdf['ShortTermMACD'] = emaCol.nDayEma(df, 12) - emaCol.nDayEma(df, 26)
        return newdf

    def createLongTermMACDcolumn(df, newdf):
        newdf['LongTermMACD'] = emaCol.nDayEma(df, 50) - emaCol.nDayEma(df, 200)
        return newdf

    def crossValidateMACD(newdf):
        newdf['MACDcv'] = newdf['ShortTermMACD'] - newdf['LongTermMACD']
        return newdf

    def getHistoDifferences(newdf):
        newdf['ShortTermSignalLine'] = newdf['ShortTermMACD'].ewm(span=9, adjust=False).mean()
        newdf['LongTermSignalLine'] = newdf['LongTermMACD'].ewm(span=9, adjust=False).mean()
        newdf['ShortTermMACDHist'] = newdf['ShortTermMACD'] - newdf['ShortTermSignalLine']
        newdf['LongTermMACDHist'] = newdf['LongTermMACD'] - newdf['LongTermSignalLine']
        newdf['HistoDiff'] = newdf['ShortTermMACDHist'] - newdf['LongTermMACDHist']
        return newdf

    def establishMACDBehaviour(df, newdf):
        emaCol.createShortTermMACDcolumn(df, newdf)
        emaCol.createLongTermMACDcolumn(df, newdf)
        emaCol.crossValidateMACD(newdf)
        emaCol.getHistoDifferences(newdf)
        return newdf


class RSI:
    def calcPriceChange(df):
        return df['Close/Last'].diff().tolist()

    def generateAverageGainLoss(df, newdf):
        gainList = []
        lossList = []
        priceChange = RSI.calcPriceChange(df)

        for item in priceChange:
            if item > 0:
                gainList.append(item)
                lossList.append(0)
            else:
                gainList.append(0)
                lossList.append(abs(item))

        gainAvg = RSI.get14DayAverage(gainList)
        lossAvg = RSI.get14DayAverage(lossList)

        relativeStrength = RSI.getRelativeStrength(gainAvg, lossAvg)
        relativeStrengthIndex = RSI.getRelativeStrengthIndex(relativeStrength)

        return RSI.writeRSItoDF(df, newdf, relativeStrengthIndex)

    def writeRSItoDF(df, newdf, RSIarray):
        newdf['RSI'] = pd.Series(RSIarray)
        return newdf

    def getRelativeStrengthIndex(relativeStrength):
        return [100 - (100 / (1 + rs)) for rs in relativeStrength]

    def getRelativeStrength(gainAvg, lossAvg):
        return np.where(lossAvg == 0, np.array(gainAvg), np.array(gainAvg) / np.array(lossAvg))

    def get14DayAverage(dataArray):
        return pd.Series(dataArray).rolling(window=14).mean().bfill().tolist()


class readableCols:
    def makeReadble(df):
        df = readableCols.addReadableRSIindicator(df)
        df = readableCols.evaluateMACDcv(df)
        return df

    def addReadableRSIindicator(df):
        df['RSIresponse'] = np.where(df['RSI'] > 70, 'Overbought', np.where(df['RSI'] < 30, 'Oversold', 'Neutral'))
        return df
    
    def evaluateMACDcv(df):
        df['MACDcvresponse'] = np.where(df['MACDcv'] > 0, 'Bullish', np.where(df['MACDcv'] < 0, 'Bearish', 'Neutral'))
        return df

class stochasticOscillator:
    def percentK(df, newdf):
        low14 = df['Low'].rolling(window=14).min()
        high14 = df['High'].rolling(window=14).max()
        
        newdf['stochOscK'] = 100 * (df['Close/Last'] - low14) / (high14 - low14)
        return newdf

    def percentD(df,newdf):
        newdf['stochOscD'] = newdf['stochOscK'].ewm(span=3, adjust=False).mean()
        return newdf
    
    def getStochOscillator(df,newdf):
        newdf = stochasticOscillator.percentK(df,newdf)
        newdf = stochasticOscillator.percentD(df,newdf)
        return newdf

class bollingerBands:
    def calculateBands(df, newdf):
        middleBand = bollingerBands.getMiddleBand(df)
        upperBand = bollingerBands.getUpperBand(df)
        lowerBand = bollingerBands.getLowerBand(df)

        newdf['middleBand'] = middleBand
        newdf['upperBand'] = upperBand
        newdf['lowerBand'] = lowerBand

        return newdf


    def getMiddleBand(df):
        return df['Close/Last'].rolling(window=20).mean()

    def getUpperBand(df):
        return df['Close/Last'].rolling(window=20).mean() + (2 * df['Close/Last'].rolling(window=20).std())

    def getLowerBand(df):
        return df['Close/Last'].rolling(window=20).mean() - (2 * df['Close/Last'].rolling(window=20).std())

def create3and5DayPercentageChange(df):
    df['3DayPercentageChange'] = df['Close'].pct_change(periods=-3)*100
    df['5DayPercentageChange'] = df['Close'].pct_change(periods=-5)*100
    df['10DayPercentageChange'] = df['Close'].pct_change(periods=-10)*100
    return df



def main(csvFilename,folder):

    df = pd.read_csv(f'{folder}/{csvFilename}')
    df = stripDollarSign(df)
    df = convertColsToFloat(df)
    

    df = df[::-1]
    
    checkDailyValuation(df)

    quantdf = pd.DataFrame()
    quantdf['Date'] = df['Date']

    quantdf = emaCol.establishMACDBehaviour(df, quantdf)
    quantdf = RSI.generateAverageGainLoss(df, quantdf)
    quantdf = stochasticOscillator.getStochOscillator(df, quantdf)
    quantdf = bollingerBands.calculateBands(df, quantdf)

    quantdf['Open'] = df['Open'].astype(float)
    quantdf['Close'] = df['Close/Last'].astype(float)

    quantdf = quantdf[::-1]
    
    quantdf = create3and5DayPercentageChange(quantdf)

    #quantdf = readableCols.makeReadble(quantdf)


    #strip the last 19 values as the have NaN values due to some averages needing 20 previous days of data
    quantdf = quantdf.iloc[:-19]




    return quantdf


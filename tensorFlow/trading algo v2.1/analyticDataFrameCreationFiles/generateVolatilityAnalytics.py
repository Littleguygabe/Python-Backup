import pandas as pd
import os
import matplotlib.pyplot as plt


class rawDataFrameClass:
    def populateDataFrameList(dataDirectory):
        dataFileNameList = os.listdir(dataDirectory)
        rawDataFrameArr = []
        for tickerFileName in dataFileNameList:
            rawDataFrameArr.append(rawDataFrameClass.getCSVfromFileName(f'{dataDirectory}/{tickerFileName}'))
        return rawDataFrameArr

    def getCSVfromFileName(tickerFileLocation):
        return (pd.read_csv(tickerFileLocation,nrows = 60))


class bollingerBands:
    def createMiddleBand(rawDataFrame, analyticDataFrame):
        analyticDataFrame['middleBollingerBand'] = rawDataFrame['Close/Last'].rolling(window=20).mean()
        return analyticDataFrame  # No need to reverse anymore

    def getStandardDeviationInClose(rawDataFrame):
        tempDf = pd.DataFrame()
        tempDf['stnd'] = rawDataFrame['Close/Last'].rolling(window=20).std()
        return tempDf  # No need to reverse anymore

    def createUpperLowerBand(rawDataFrame, analyticDataFrame):
        tempDf = bollingerBands.getStandardDeviationInClose(rawDataFrame)
        analyticDataFrame['upperBollingerBand'] = analyticDataFrame['middleBollingerBand'] + 2 * tempDf['stnd']
        analyticDataFrame['lowerBollingerBand'] = analyticDataFrame['middleBollingerBand'] - 2 * tempDf['stnd']
        return analyticDataFrame

    def createBollingerBands(rawDataFrame, analyticDataframe):
        # DataFrame already reversed once when first loaded, no need to reverse again
        analyticDataframe = bollingerBands.createMiddleBand(rawDataFrame, analyticDataframe)
        analyticDataframe = bollingerBands.createUpperLowerBand(rawDataFrame, analyticDataframe)

        # Keep the newest data at the bottom by reversing back the analytics dataframe
        analyticDataframe = analyticDataframe.iloc[::-1].reset_index(drop=True)

        return analyticDataframe

    def plotBollingerBands(rawDataFrame, analyticDataFrame):
        analyticDataFrame['Date'] = pd.to_datetime(analyticDataFrame['Date'])  # Convert Date to datetime

        plt.plot(analyticDataFrame['Date'].iloc[::-1], analyticDataFrame['middleBollingerBand'].iloc[::-1], label='Middle Band', color='blue')
        plt.plot(analyticDataFrame['Date'].iloc[::-1], analyticDataFrame['upperBollingerBand'].iloc[::-1], label='Upper Band', color='green')
        plt.plot(analyticDataFrame['Date'].iloc[::-1], analyticDataFrame['lowerBollingerBand'].iloc[::-1], label='Lower Band', color='red')
        plt.plot(analyticDataFrame['Date'].iloc[::-1], rawDataFrame['Close/Last'], label='Close Price', color='black')

        plt.xticks(rotation=45)
        plt.legend()
        plt.show()

    def createBollingerBandWidth(analyticsdf):
        analyticsdf['bandWidth'] = (analyticsdf['upperBollingerBand']-analyticsdf['lowerBollingerBand'])
 
        return analyticsdf

    def getScaledBBWpct(rawDataFrame,analyticsdf):
        reversedRawDf = rawDataFrame.iloc[::-1].copy()
        reversedRawDf.reset_index(drop=True, inplace=True)

        analyticsdf = bollingerBands.createBollingerBandWidth(analyticsdf)
        analyticsdf['normalisedBBWpct'] = (analyticsdf['bandWidth']/reversedRawDf['Close/Last'])*100

        return analyticsdf

class averageTrueRange:
    def createAverageTrueRange(rawDataFrame, analyticsDataFrame):
        highPrevCloseDifdf = averageTrueRange.getHighPrevCloseDif(rawDataFrame)
        lowPrevCloseDifdf = averageTrueRange.getLowPrevCloseDif(rawDataFrame)
        highLowDifdf = averageTrueRange.getHighLowDif(rawDataFrame)

        rangesDf = pd.concat([highLowDifdf, lowPrevCloseDifdf, highPrevCloseDifdf], axis=1)
        rangesDf = averageTrueRange.getTrueRange(rangesDf)
        rangesDf = averageTrueRange.getAverageTrueRange(rangesDf)

        # Reverse it back before assigning to ensure the newest data is at the bottom
        analyticsDataFrame['averageTrueRange'] = rangesDf['averageTrueRange'].iloc[::-1].reset_index(drop=True)

        return analyticsDataFrame

    def getAverageTrueRange(rangesDf):
        rangesDf['averageTrueRange'] = rangesDf['trueRange'].rolling(window=14).mean()
        return rangesDf

    def getTrueRange(rangesDataFrame):
        rangesDataFrame['trueRange'] = rangesDataFrame[['highPrevCloseDif', 'lowPrevCloseDif', 'highLowDif']].max(axis=1)
        return rangesDataFrame

    def getHighPrevCloseDif(rawDataFrame):
        tempdf = pd.DataFrame()
        tempdf['highPrevCloseDif'] = (rawDataFrame['High'] - rawDataFrame['Close/Last'].shift(-1)).abs()
        return tempdf

    def getLowPrevCloseDif(rawDataFrame):
        tempdf = pd.DataFrame()
        tempdf['lowPrevCloseDif'] = (rawDataFrame['Low'] - rawDataFrame['Close/Last'].shift(-1)).abs()
        return tempdf

    def getHighLowDif(rawDataFrame):
        tempdf = pd.DataFrame()
        tempdf['highLowDif'] = rawDataFrame['High'] - rawDataFrame['Low']
        return tempdf

    def getScaledATRpct(rawDataFrame,analyticsdf):
        rawDataFrame = rawDataFrame.copy().iloc[::-1]

        analyticsdf['normalisedATRpct'] = (analyticsdf['averageTrueRange']/rawDataFrame['Close/Last'])*100

        return analyticsdf

    def plot(rawDataFrame,analyticsDataFrame):
        reversedAnalayticDf = analyticsDataFrame.copy().iloc[::-1]
        plt.plot(reversedAnalayticDf['Date'],reversedAnalayticDf['averageTrueRange']*10,label = 'ATR x10')
        plt.plot(reversedAnalayticDf['Date'],rawDataFrame['Close/Last'],label = 'close')

        plt.legend()
        plt.show()


def copyDates(rawdf, analyticdf):
    # Copy the reversed Date from rawdf to analyticdf
    analyticdf['Date'] = rawdf['Date']  # Date was reversed only once during initial load
    return analyticdf

def sortHighBBWLowATR(analyticsDf):
    analyticsDf['BBWATRmetric'] = analyticsDf['normalisedBBWpct']*+((1/analyticsDf['normalisedATRpct']))

    ATRBBWsortedADF = analyticsDf.sort_values(by='BBWATRmetric',ascending=False)
    return ATRBBWsortedADF

def createAnalyticDataFrame(dataDirectory):
    dataFrameList = rawDataFrameClass.populateDataFrameList(dataDirectory)
    finalisedAnalyticDataFramesArr = []

    for rawDataFrame in dataFrameList:
        # Reverse the rawDataFrame once when first loaded
        rawDataFrame = rawDataFrame.iloc[::-1].reset_index(drop=True)

        analyticDataFrame = pd.DataFrame()
        analyticDataFrame = copyDates(rawDataFrame, analyticDataFrame)
        analyticDataFrame = bollingerBands.createBollingerBands(rawDataFrame, analyticDataFrame)
        analyticDataFrame = bollingerBands.getScaledBBWpct(rawDataFrame, analyticDataFrame)

        analyticDataFrame = averageTrueRange.createAverageTrueRange(rawDataFrame, analyticDataFrame)
        analyticDataFrame = averageTrueRange.getScaledATRpct(rawDataFrame, analyticDataFrame)

        # Add the ticker symbol to the analyticDataFrame
        #analyticDataFrame['symbol'] = rawDataFrame['symbol'].iloc[0]  # Assuming the symbol is in the rawDataFrame

        sortHighBBWLowATR(analyticDataFrame)

        #averageTrueRange.plot(rawDataFrame, analyticDataFrame)
        #bollingerBands.plotBollingerBands(rawDataFrame, analyticDataFrame)

        finalisedAnalyticDataFramesArr.append(analyticDataFrame)

    return finalisedAnalyticDataFramesArr

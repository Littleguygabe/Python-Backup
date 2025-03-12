import pandas as pd
import os

#candleSticks and volume -> wide candlesticks and large volume shows increasing momentum

class rawDataFrameClass:
    def populateDataFrameList(dataDirectory):
        dataFileNameList = os.listdir(dataDirectory)
        rawDataFrameArr = []
        for tickerFileName in dataFileNameList:
            rawDataFrameArr.append(rawDataFrameClass.getCSVfromFileName(f'{dataDirectory}/{tickerFileName}'))
        return rawDataFrameArr

    def getCSVfromFileName(tickerFileLocation):
        return pd.read_csv(tickerFileLocation,nrows = 60)

class candleSticks:
    def generateCandleSticks(rawdf,analyticsDataFrame):
        analyticsDataFrame['ABScandleStickRangeVal'] = (rawdf['Close/Last']-rawdf['Open']).abs()

        return analyticsDataFrame

class volume:
    def getVolTraded(rawdf,analyticsdf):
        analyticsdf['Volume'] = rawdf['Volume']

        return analyticsdf
    
    def get20DayVolTradedEMA(analyticsdf):
        analyticsdf['volTraded20EMA'] = analyticsdf['Volume'].ewm(span=20,adjust=False).mean()
        return analyticsdf   

    def getEMAVolPctDif(analyticsdf):
        analyticsdf['EMAvolPctDif'] = ((analyticsdf['Volume']-analyticsdf['volTraded20EMA'])/analyticsdf['volTraded20EMA'])*100
        return analyticsdf

    def calculateVolumeMomentumPct(rawdf,analyticsdf):
        #calculates the percentage difference between the current day's volume traded and the 20 day EMA of volume change to show if momentum is increasing and how quickly
        analyticsdf = volume.getVolTraded(rawdf,analyticsdf)
        analyticsdf = volume.get20DayVolTradedEMA(analyticsdf)
        analyticsdf = volume.getEMAVolPctDif(analyticsdf)

        return analyticsdf

def calculateVolCSmetric(analyticDf):
    analyticDf['volCsMetric'] = analyticDf['ABScandleStickRangeVal']*analyticDf['EMAvolPctDif']
    return analyticDf

def getMomentumAnalytics(dataDirectory):
    dataframeList = rawDataFrameClass.populateDataFrameList(dataDirectory)
    finalisedAnalyticDataFramesArr = []

    for rawdf in dataframeList:

        rawdf = rawdf.iloc[::-1].reset_index(drop=True)
        
        analyticDataFrame = pd.DataFrame()
        analyticDataFrame = candleSticks.generateCandleSticks(rawdf,analyticDataFrame)
        analyticDataFrame = volume.calculateVolumeMomentumPct(rawdf,analyticDataFrame)
        analyticDataFrame = calculateVolCSmetric(analyticDataFrame)

        analyticDataFrame = analyticDataFrame.iloc[::-1].reset_index(drop=True)
        finalisedAnalyticDataFramesArr.append(analyticDataFrame)


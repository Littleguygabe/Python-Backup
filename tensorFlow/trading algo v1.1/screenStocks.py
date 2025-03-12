import math
import pandas as pd
import trainStockNNfiles.dataRead as dataRead
import os
from tensorflow import keras

modelVersion = '1.04'

def createPredictionsDataFrame():
    arrOfPredictableDataFrames = getPredictableDataFrames()
    for i in range(len(arrOfPredictableDataFrames)):
        arrOfPredictableDataFrames[i] = arrOfPredictableDataFrames[i].iloc[:1]

    return arrOfPredictableDataFrames

def getPredictableDataFrames():
    fileList = os.listdir('stocksToPredict')
    predictableDataFrames = []

    for i in range(len(fileList)):
        predictableDataFrames.append(dataRead.main(fileList[i],'stocksToPredict'))
        #strip the percentage change and date columns as dont need for predicting
        predictableDataFrames[i] = predictableDataFrames[i].drop(columns=['3DayPercentageChange','5DayPercentageChange','10DayPercentageChange'])

    return predictableDataFrames

def loadModel(modelVersion):
    model = keras.models.load_model(f'models/model_{modelVersion}.keras')
    return model

def generatePredictions(predictableDataFrames, model):
    predictionsArr = []
    for dataFrame in predictableDataFrames:
        predictionsArr.append(model.predict(dataFrame.drop(columns=['Date'])))

    return predictionsArr

def convertPredictionsToActualValues(predictionsForSingleStock, dataFrame):
    ClosePrice = dataFrame['Close'].iloc[0]  # Get the current Close price
    predictionValues = []

    # Convert each predicted percentage to actual price change
    for prediction in predictionsForSingleStock:
        # Need to divide by 10,000 to get the percentage
        predictedValue = (1 + (prediction / 10000)) * ClosePrice  # Convert percentage to actual price
        predictionValues.append(predictedValue)

    # Return the actual price values (include the initial close price at the start)
    formattedPredictionValues = [ClosePrice] + predictionValues
    return formattedPredictionValues


def getDatesForPredictions(stockdf, predictionDays):
    dates = []
    currentDate = stockdf['Date'].iloc[0]
    dates.append(pd.to_datetime(currentDate))
    for daysInFuture in predictionDays:
        dates.append(pd.to_datetime(currentDate) + pd.Timedelta(days=daysInFuture))

    return dates

# Removed plot functions as you no longer need plotting
# def plotIndividualStock(predictionsForSingleStock, stockdf): ...
# def plotPreviousNDaysValue(stockdf, n): ...
# def plotPredictions(predictionsArr, DataFrameArr, fullDataframesArr): ...

def getRawDataframes():
    fileList = os.listdir('stocksToPredict')
    rawDataframes = []
    for file in fileList:
        rawDataframes.append(pd.read_csv(f'stocksToPredict/{file}'))
    return rawDataframes

def getNumberOfStocksToChoose(stockComparisondf, percentageToKeep):
    noStocks = len(stockComparisondf)
    noStocks *= (percentageToKeep / 100)
    return int(math.ceil(noStocks)) 

def getWeightedPercentageIncrease(stockPctChangeArr):
    pctWeights = [2,1,0.5]
    pctChangesArr = stockPctChangeArr[0]
    totalPctChange = 0
    for pctChange,weight in zip(pctChangesArr,pctWeights):
        totalPctChange+=pctChange*weight

    return totalPctChange/len(pctWeights) 

def getArrofSymbolsFromDfArray(rawDfArray):
    ArrOfSymbols = []
    for dataFrame in rawDfArray:
        ArrOfSymbols.append(dataFrame['symbol'].iloc[0])

    return ArrOfSymbols

def zipStockSymbolWeightedPctChange(rawDfArray,weightedPctChangeArr):
    newDf = pd.DataFrame()
    newDf['symbol'] = getArrofSymbolsFromDfArray(rawDfArray)
    newDf['weightedPctChange'] = weightedPctChangeArr

    return newDf

def getBestNPercentofDataFrames(predictionsArr, n):
    rawDfArray = getRawDataframes()
    weightedPctChangeArr = []

    n = math.ceil(len(rawDfArray)*(n/100))

    for stockPctChange in predictionsArr:
        weightedPctChangeArr.append(getWeightedPercentageIncrease(stockPctChange))

    symbolWeightedPctChangeDf = zipStockSymbolWeightedPctChange(rawDfArray,weightedPctChangeArr)
    symbolWeightedPctChangeDf = symbolWeightedPctChangeDf.sort_values(by='weightedPctChange',ascending=False)
    bestPerformingStocks = symbolWeightedPctChangeDf.iloc[:n]
    
    return bestPerformingStocks


def predictStocks():
    arrOfPredictableDataFrames = createPredictionsDataFrame()


    model = loadModel(modelVersion)

    predictionsArr = generatePredictions(arrOfPredictableDataFrames, model)

    # Now, get the best stock options without plotting
    bestStockoptions = getBestNPercentofDataFrames(predictionsArr, 10)

    return bestStockoptions

    # Plot graph data removed since you no longer need it
    # if plotGraphData:
    #     plotPredictions(predictionsArr, arrOfPredictableDataFrames, getRawDataframes())


import numpy as np
import pandas as pd
import joblib
from tensorflow import keras
import trainBuyNeuralNetowrkFiles.dataRead as dataRead


def loadModel():
    model = keras.models.load_model('trainBuyNeuralNetowrkFiles/buyNNmodel.keras')
    return model

def getListOfTickers(dataframe):
    tickerList = dataframe['symbol'].to_list()
    return tickerList

def loadScaler():
    scaler = joblib.load('trainBuyNeuralNetowrkFiles/buyScaler.pkl')
    return scaler

def dropAllButMostRecentData(dataFrame):
    dataFrame = dataFrame.iloc[[0]]
    return dataFrame

def createPredictions(model,riskAnalysisDataFrameList):
    predictionsArr = []
    scaler = loadScaler()
    

    for data in riskAnalysisDataFrameList:
        dataFrame = data[1].drop(columns=['Date'],axis=1)
        dataFrame = dropAllButMostRecentData(dataFrame)
        dataFrameScaled = scaler.transform(dataFrame)
        predictions = model.predict(dataFrameScaled)
        print(predictions[0][0])
        predictionsArr.append([data[0],np.argmax(predictions)])

    return predictionsArr

def runRiskAnalysis(dataframe):
    model = loadModel()
    listOfTopTickers = getListOfTickers(dataframe)

    riskAnalysisDataFrameList = dataRead.retrieveData(['stocksToPredict',listOfTopTickers]) 

    predictionsArr = createPredictions(model,riskAnalysisDataFrameList)
    print(predictionsArr)
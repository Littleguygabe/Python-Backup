import pandas as pd
import numpy as np
import os

import tensorflow
from tensorflow.keras.layers import Dense


def getCSVfilenameList():
    strippedFileNameList = []
    
    fileList = os.listdir('Analytics/stockResults')
    for fileName in fileList:
        strippedName,extension = os.path.splitext(fileName)
        if extension=='.csv':
            strippedFileNameList.append(strippedName)

    return strippedFileNameList

def getMostRecentModelversion(strippedFileNameList):
    fileNameAsFloatList = []
    for file in strippedFileNameList:
        try:
            fileNameAsFloatList.append(float(file))

        except:
            pass

    return fileNameAsFloatList

def incrementModelVersion(floatFileNameList):
    if len(floatFileNameList) == 0:
        return 1

    currentVersion = max(floatFileNameList)
    return currentVersion+0.01

def getNextModelVersion():
    strippedFileNameList = getCSVfilenameList()
    floatFileNameList = getMostRecentModelversion(strippedFileNameList)
    nextModelVersion = incrementModelVersion(floatFileNameList)
    
    return nextModelVersion

def createStockDataFrame(DataArray):
    stockdf = pd.DataFrame()
    stockdf['StockID'] = DataArray[0]
    stockdf['MAE test loss (accuracy)'] = DataArray[2]
    stockdf['train test loss dif %'] = DataArray[3]
    stockdf['fit'] = np.where(stockdf['train test loss dif %']>1,'Overfitting',np.where(stockdf['train test loss dif %']>-1,'Marginal','Underfitting'))

    return stockdf

def storeStockData(stockDataArray): #[csvFileList,modelVersion,val_lossList,trainTestLossPercentageDifList]
    modelVersion = stockDataArray[1]
    stockdf = createStockDataFrame(stockDataArray)

    stockdf.to_csv(f'Analytics/stockResults/{modelVersion}.csv',index=False)

def getNumberOfDataPoints(csvFileList,folder):
    NdataPoints = 0
    for fileName in csvFileList:
        loadedDf = pd.read_csv(f'{folder}/{fileName}')

        NdataPoints+=len(loadedDf)


    return NdataPoints

def getAvgAccuracy(accuracyList):
    return sum(accuracyList)/len(accuracyList)

def getLayerStrcuture(model):
    structure = []
    for layer in model.layers:
        if isinstance(layer,Dense):
            structure.append(layer.units)

    return structure


def createModelDataFrame(dataArray):
    modeldf = pd.DataFrame()

    NdataPoints = getNumberOfDataPoints(dataArray[6],dataArray[11])
    modeldf['Version'] = [dataArray[0]]
    modeldf['Dropout Rate'] = [dataArray[1]]
    modeldf['Init learn rate'] = [dataArray[2]]
    modeldf['batchSize'] = [dataArray[3]]
    modeldf['Nepochs'] = [dataArray[4]]

    modeldf['train/test split'] = [f'{1-dataArray[5]}/{dataArray[5]}']
    modeldf['avg accuracy (%)'] = [getAvgAccuracy(dataArray[7])]
    modeldf['No data points'] = [NdataPoints]
    modeldf['Training time (s)'] = [f'{dataArray[8]//60}m {dataArray[8]%60}s']
    modeldf['avg train/test loss dif'] = [sum(dataArray[9])/len(dataArray[9])]
    modeldf['No Layers'] = [len(dataArray[10].layers)]
    modeldf['Layer Struct'] = [getLayerStrcuture(dataArray[10])]

    return modeldf

def storeModelData(modelDataArray): #modelVersion,dropoutRate,learningRate,batchSize,Nepochs,testSize,csvFileList,val_lossList,(time.time()-startTime),trainTestLossPercentageDifList,model,trainingFolder 

    modeldf = createModelDataFrame(modelDataArray)
    modeldf.to_csv('Analytics/modelAnalytics.csv',index=False,header=False,mode='a')
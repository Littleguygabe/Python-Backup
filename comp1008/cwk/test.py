import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

import numpy as np
import matplotlib.pyplot as plt

def countDuplicateRows(df):
    dupeCount = df.duplicated().sum()
    return dupeCount

def countNaNRows(df):
    NaNCount = df.isna().any(axis=1).sum()
    return NaNCount

def countOutlierRows(df,rangeCoeff) -> pd.DataFrame:
    quart1 = df.quantile(0.25)
    quart3 = df.quantile(0.75)

    IQrange = quart3 - quart1

    lowerBound = quart1-rangeCoeff*IQrange
    upperBound = quart3+rangeCoeff*IQrange

    outlierCount = ((df<lowerBound) | (df>upperBound)).any(axis=1).sum()

    return outlierCount

class NaNhandling:
    def handleNaNmodal(self, df):
        return df.apply(lambda x: x.fillna(x.mode()[0], axis=0))

    def handleNaNdrop(self, df):
        return df.dropna()

    def handleNaNValues(self, df):
        handleMethod = 'drop'

        if countNaNRows(df) == 0:
            return df

        if handleMethod == 'modal':
            return self.handleNaNmodal(df)
        elif handleMethod == 'drop':
            return self.handleNaNdrop(df)

class outlierHandling:
    def getUpperLowerBounds(self, df,rangeCoeff):
        
        quart1 = df.quantile(0.25)
        quart3 = df.quantile(0.75)

        IQrange = quart3 - quart1
        
        lowerBound = quart1-rangeCoeff*IQrange
        upperBound = quart3+rangeCoeff*IQrange
        
        return lowerBound, upperBound

    def handleOutliersModal(self, df,rangeCoeff):
        lowerBound, upperBound = self.getUpperLowerBounds(df,rangeCoeff)
        

        for col in df.columns:
            modalVal = df[col].mode()[0]
            df[col] = df[col].apply(lambda x: modalVal if (x < lowerBound[col] or x > upperBound[col]) else x)

        return df

    def handleOutliersDrop(self, df,rangeCoeff):
        lowerBound, upperBound = self.getUpperLowerBounds(df,rangeCoeff)
        return df[~((df < lowerBound) | (df > upperBound)).any(axis=1)]

    def handleOutliers(self, df,rangeCoeff):
        handleMethod = 'drop'

        if countOutlierRows(df,rangeCoeff) == 0:
            return df

        if handleMethod == 'modal':
            return self.handleOutliersModal(df,rangeCoeff)


        elif handleMethod == 'drop':
            return self.handleOutliersDrop(df,rangeCoeff)

class preProcessing(NaNhandling, outlierHandling):
    def __init__(self, df, rc):
        super().__init__()
        self.df = df
        self.rangeCoeff = rc
        self.performPreProcessing()

    def performPreProcessing(self):
        self.df = self.handleNaNValues(self.df)
        self.df = self.handleOutliers(self.df,self.rangeCoeff)
        self.df = self.removeDuplicateRows()

    def removeDuplicateRows(self):
        return self.df.drop_duplicates()


def runTraining(wineQualDf):
    min_max_scaler = preprocessing.MinMaxScaler()

    X = wineQualDf.drop(columns=['quality'])
    y = wineQualDf[['quality']]

    XScaled = min_max_scaler.fit_transform(X)

    Xtrain, Xtest, ytrain, ytest = train_test_split(XScaled, y, test_size=0.3, random_state=42)

    model = LinearRegression()
    model.fit(Xtrain, ytrain)
    yPred = model.predict(Xtest)

    mse = mean_squared_error(ytest, yPred)
    mae = mean_absolute_error(ytest, yPred)
    r2 = r2_score(ytest, yPred)


    #print(f'mse: {round(mse, 5)}')
    #print(f'mae: {round(mae, 5)}')
    #print(f'Rsquared score: {round(r2, 5)}')



    return round(mse,15),round(mae,15),round(r2,15)

def plotLoBF(rangeCoeffsToCheck,data,color): 
    coefficients = np.polyfit(rangeCoeffsToCheck,data,3)
    polynomial = np.poly1d(coefficients)
    xfit = np.linspace(rangeCoeffsToCheck.min(),rangeCoeffsToCheck.max(),100)
    yfit = polynomial(xfit)

    plt.plot(xfit,yfit,color=color,alpha=1)

if __name__ == '__main__':


    maes = []
    mses = []
    r2s = []

    rangeCoeffsToCheck = np.arange(1,15,0.1)

    for rangeCoeff in rangeCoeffsToCheck:
        wineQualDf = pd.read_csv('winequality-red.csv')
        wineQualDf = preProcessing(wineQualDf,rangeCoeff).df
        mse,mae,r2 = runTraining(wineQualDf)
        maes.append(mae)
        mses.append(mse)
        r2s.append(r2)
    
    print(maes)
    print(mses)
    print(r2s)

    plt.scatter(rangeCoeffsToCheck,mses,marker = 'x',color='blue',alpha = 1)
    plt.scatter(rangeCoeffsToCheck,maes,marker = 'x',color='red',alpha=1)
    plt.scatter(rangeCoeffsToCheck,r2s,marker = 'x',color='orange',alpha=1)
    
    plotLoBF(rangeCoeffsToCheck,mses,'blue')
    plotLoBF(rangeCoeffsToCheck,maes,'red')
    plotLoBF(rangeCoeffsToCheck,r2s,'orange')


    plt.show()



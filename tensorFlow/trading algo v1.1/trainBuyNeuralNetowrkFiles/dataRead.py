import pandas as pd
import os
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

weights = {
    'TrueRange': 0.1,
    'averageTrueRange': 0.1,
    'bollingerBandWidth': 0.2,
    'averageDirectionalIndex': 0.2,
    'relativeStrengthIndex': 0.15,
    'maxDrawdown': 0.2,
    'minMaxVolTradedDif': 0.05
}

scaler = StandardScaler()

def createTrueRange(df):
    """Calculates True Range (TR) and returns a DataFrame."""
    df = df[::-1].copy()  # Reverse to ensure correct shift()

    tr1 = df['High'] - df['Low']
    tr2 = (df['High'] - df['Close/Last'].shift(1)).abs()
    tr3 = (df['Low'] - df['Close/Last'].shift(1)).abs()

    # Compute True Range
    analyticsDf = pd.DataFrame()
    analyticsDf['Date'] = df['Date']
    analyticsDf['TrueRange'] = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    return analyticsDf[::-1]  # Reverse back to original order

def getNdayATR(analyticsDf, n):
    """Computes ATR using an N-day EMA and returns a DataFrame."""
    analyticsDf['averageTrueRange'] = analyticsDf['TrueRange'].ewm(span=n, adjust=False).mean()
    return analyticsDf

def createAverageTrueRangeCol(df):
    """Creates ATR column from stock data DataFrame."""
    analyticsDf = createTrueRange(df)
    analyticsDf = getNdayATR(analyticsDf, 14)
    return analyticsDf

def createBollingerWidthCol(df, riskAnalysisDf):
    """Creates Bollinger Band Width column and appends it to the risk DataFrame."""
    bandValues = pd.DataFrame()  # Will be sorted with oldest first, so need to flip before adding to the risk df

    df = df[::-1].copy()
    bandValues['middleBand'] = df['Close/Last'].rolling(window=20).mean()
    bandValues['stndD'] = df['Close/Last'].rolling(window=20).std()

    bandValues['upperBand'] = bandValues['middleBand'] + 2 * bandValues['stndD']
    bandValues['lowerBand'] = bandValues['middleBand'] - 2 * bandValues['stndD']

    bandValues['bollingerBandWidth'] = (bandValues['upperBand'] - bandValues['lowerBand']) / bandValues['middleBand']

    bandValues = bandValues[::-1]
    riskAnalysisDf['bollingerBandWidth'] = bandValues['bollingerBandWidth']

    return riskAnalysisDf

def createAverageDirectionalIndexCol(df, riskAnalyticsdf):
    """Creates Average Directional Index column for trend strength."""
    df = df[::-1].copy()
    riskAnalyticsdf = riskAnalyticsdf[::-1].copy()
    
    tempdf = pd.DataFrame()  # As riskdf has been flipped, concat then flip the resulting riskdf

    tempdf['upMove'] = df['High'].diff()
    tempdf['downMove'] = -df['Low'].diff()

    # Calculate +DI and -DI using rolling windows
    tempdf['+DI'] = tempdf['upMove'].rolling(window=14).sum() / riskAnalyticsdf['averageTrueRange']
    tempdf['-DI'] = tempdf['downMove'].rolling(window=14).sum() / riskAnalyticsdf['averageTrueRange']   

    # Calculate Average Directional Index and assign it properly
    riskAnalyticsdf['averageDirectionalIndex'] = abs(tempdf['+DI'] - tempdf['-DI']).rolling(window=14).mean()

    return riskAnalyticsdf[::-1]  # Reverse back to original order

def createRelativeStrengthIndexCol(df,riskAnalyticsDf):
    df = df[::-1].copy()
    tempdf = pd.DataFrame()
    riskAnalyticsDf = riskAnalyticsDf[::-1].copy()

    tempdf['priceChange'] = df['High'].diff()
    tempdf['gain'] = tempdf['priceChange'].where(tempdf['priceChange']>0,0)
    tempdf['loss'] = -tempdf['priceChange'].where(tempdf['priceChange']<0,0)

    tempdf['avgGain'] = tempdf['gain'].rolling(window=14).mean()
    tempdf['avgLoss'] = tempdf['loss'].rolling(window=14).mean()

    tempdf['relativeStrength'] = tempdf['avgGain']/tempdf['avgLoss']

    riskAnalyticsDf['relativeStrengthIndex'] = 100 - (100/(1+tempdf['relativeStrength']))

    return riskAnalyticsDf[::-1]

def createMaxDrawdownCol(df,riskAnalyticsDf):
    df = df[::-1].copy()
    tempdf = pd.DataFrame()
    riskAnalyticsDf = riskAnalyticsDf[::-1].copy()

    tempdf['maxPriceSoFar'] = df['Close/Last'].cummax()
    tempdf['drawdown'] = (df['Close/Last'] - tempdf['maxPriceSoFar']) / tempdf['maxPriceSoFar']

    riskAnalyticsDf['maxDrawdown'] = tempdf['drawdown'].rolling(window=30).min()

    return riskAnalyticsDf[::-1]

def createMaxDailyVolumeDifferenceCol(df,riskAnalyticsDf):
    df = df[::-1].copy()
    riskAnalyticsDf = riskAnalyticsDf[::-1].copy()

    tempDf = pd.DataFrame()
    tempDf['maxVolTradedOver30Days'] = df['Volume'].rolling(window=30).max()
    tempDf['minVolTradedOver30Days'] = df['Volume'].rolling(window=30).min()

    riskAnalyticsDf['minMaxVolTradedDif'] = tempDf['maxVolTradedOver30Days'] - tempDf['minVolTradedOver30Days']

    return riskAnalyticsDf[::-1]

def normaliseColumn(df,colName):

    #df[colName] = scaler.fit_transform(df[[colName]])

    minVal = df[colName].min()
    maxVal = df[colName].max()

    return (df[colName]-minVal)/(maxVal-minVal)
    #return df[colName]

def createNormalisedRiskScore(riskAnalyticsDf):
    ### improvement
    # the signal is being generated off of the normalised values within the stock data set rather
    # than the the major data set with all stocks

    normalisedRiskdf = pd.DataFrame()
    normalisedRiskdf['normalisedTrueRange'] = normaliseColumn(riskAnalyticsDf,'TrueRange')
    normalisedRiskdf['normalisedAverageTrueRange'] = normaliseColumn(riskAnalyticsDf,'averageTrueRange')   
    normalisedRiskdf['normalisedBollingerBandWidth'] = normaliseColumn(riskAnalyticsDf,'bollingerBandWidth')
    normalisedRiskdf['normalisedAverageDirectionalIndex'] = normaliseColumn(riskAnalyticsDf,'averageDirectionalIndex')
    normalisedRiskdf['normalisedRelativeStrengthIndex'] = normaliseColumn(riskAnalyticsDf,'relativeStrengthIndex')
    normalisedRiskdf['normalisedMaxDrawdown'] = normaliseColumn(riskAnalyticsDf,'maxDrawdown')
    normalisedRiskdf['normalisedMinMaxVolTradedDif'] = normaliseColumn(riskAnalyticsDf,'minMaxVolTradedDif')
    normalisedRiskdf['normalisedRiskScore'] = (
        normalisedRiskdf['normalisedTrueRange'] * weights['TrueRange'] +
        normalisedRiskdf['normalisedAverageTrueRange'] * weights['averageTrueRange'] +
        normalisedRiskdf['normalisedBollingerBandWidth'] * weights['bollingerBandWidth'] +
        normalisedRiskdf['normalisedAverageDirectionalIndex'] * weights['averageDirectionalIndex'] +
        normalisedRiskdf['normalisedRelativeStrengthIndex'] * weights['relativeStrengthIndex'] +
        normalisedRiskdf['normalisedMaxDrawdown'] * weights['maxDrawdown'] +
        normalisedRiskdf['normalisedMinMaxVolTradedDif'] * weights['minMaxVolTradedDif']
    )
        
    normalisedRiskdf['normalisedRiskScore'] = normaliseColumn(normalisedRiskdf,'normalisedRiskScore')
    return normalisedRiskdf


def createSignalCol(riskAnalyticsDf):
    normalisedRiskAnalyticsDf = createNormalisedRiskScore(riskAnalyticsDf)
    riskAnalyticsDf['riskLevel'] = ((normalisedRiskAnalyticsDf['normalisedRiskScore']*99)+1).round()

    return riskAnalyticsDf

def retrieveData(args):
    """Reads stock data from CSV, processes, and appends risk metrics."""

    globalDataFrame = pd.DataFrame()


    if len(args) == 1:
        tickers = os.listdir(args[0])
        for fileName in tickers:

            df = pd.read_csv(f'{args[0]}/{fileName}')
            riskAnalyticsDf = createAverageTrueRangeCol(df)
            riskAnalyticsDf = createBollingerWidthCol(df, riskAnalyticsDf)
            riskAnalyticsDf = createAverageDirectionalIndexCol(df, riskAnalyticsDf)
            riskAnalyticsDf = createRelativeStrengthIndexCol(df,riskAnalyticsDf)
            riskAnalyticsDf = createMaxDrawdownCol(df,riskAnalyticsDf)
            riskAnalyticsDf = createMaxDailyVolumeDifferenceCol(df,riskAnalyticsDf)
            riskAnalyticsDf = riskAnalyticsDf.iloc[:-29]
            
            

            globalDataFrame = pd.concat([globalDataFrame,riskAnalyticsDf],axis=0,ignore_index=True)
        

        globalDataFrame = createSignalCol(globalDataFrame) #call with the global data set

        return globalDataFrame # Ensure most recent is at the top

    else:
        riskAnlysisArr = []
        folder = args[0]
        tickers = args[1]
        for ticker in tickers:
            df = pd.read_csv(f'{folder}/{ticker}.csv')
            riskAnalyticsDf = createAverageTrueRangeCol(df)
            riskAnalyticsDf = createBollingerWidthCol(df, riskAnalyticsDf)
            riskAnalyticsDf = createAverageDirectionalIndexCol(df, riskAnalyticsDf)
            riskAnalyticsDf = createRelativeStrengthIndexCol(df,riskAnalyticsDf)
            riskAnalyticsDf = createMaxDrawdownCol(df,riskAnalyticsDf)
            riskAnalyticsDf = createMaxDailyVolumeDifferenceCol(df,riskAnalyticsDf)
            riskAnalyticsDf = riskAnalyticsDf.iloc[:-29]           
            
            riskAnlysisArr.append([ticker,riskAnalyticsDf])

        return riskAnlysisArr
        

if __name__ == '__main__':
    dataframe = retrieveData('nasdaq100')
    print(dataframe)
# currently being normalised before the being put into the neural network
    #may result in incosistent risk values -> but can potentially change later if issues arise
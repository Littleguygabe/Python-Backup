import generateAnalytics as ga
import pandas as pd
import os 



indicatorSaveFolder = 'indicatorsTrainingData'

def getindicators(stockDataFolder,file):
    rawdf = pd.read_csv(f'{stockDataFolder}/{file}')
    indicators = ga.main(rawdf[::-1])
    return indicators

def getFileList(stockDataFolder):
    fileList = os.listdir(stockDataFolder)
    return fileList

def main():
    stockDataFolder = 'nasdaq100'

    count = 1
    NoStocks = len(getFileList(stockDataFolder))

    for file in getFileList(stockDataFolder):
        indicators = getindicators(stockDataFolder,file)
        symbol = os.path.splitext(file)[0]       
        indicators.to_csv(f'{indicatorSaveFolder}/{symbol.upper()}.csv')    

        print(f'stock {count}/{NoStocks}')
        count+=1




if __name__ == '__main__':
    main()
import generateAnalytics as ga
import pandas as pd
import os 



indicatorSaveFolder = 'indicatorData'

def getindicators(stockDataFolder,file):
    rawdf = pd.read_csv(f'{stockDataFolder}/{file}')
    indicators = ga.main(rawdf[::-1])
    return indicators

def getFileList(stockDataFolder):
    fileList = os.listdir(stockDataFolder)
    return fileList

def main():
    stockDataFolder = 'nasdaq100'

    for file in getFileList(stockDataFolder):
        indicators = getindicators(stockDataFolder,file)
        print(indicators)





if __name__ == '__main__':
    main()
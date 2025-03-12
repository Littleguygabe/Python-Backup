import os
import marketSim as ms
import pandas as pd
import generateAnalytics as ga

dataFolder = 'backtestingData'

def main(myPortfolio):
    fileList = os.listdir(dataFolder)
    for file in fileList:
        rawdf = pd.read_csv(f'{dataFolder}/{file}')
        analyticdf = ga.main(rawdf[::-1])  



if __name__ == '__main__':
    main(ms.Portfolio())
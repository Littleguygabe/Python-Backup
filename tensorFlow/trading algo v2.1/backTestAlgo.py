import main as tradingAlgo
import marketSim as ms
import os
import pandas as pd
import time
#myportfolio = ms.Portfolio()

## need to create the restricted data from the nasdaq 100 files and put into a
## back testing folder so its as if the data is real time

def runBackTesting():
    
    myPortfolio = ms.Portfolio()
    fileList = os.listdir('nasdaq100') #folder to gen test data from
    dirDfArr = []
    for file in fileList:
        dirDfArr.append([file,pd.read_csv(f'nasdaq100/{file}')])

    # only read the directory once to optimise speed
    count = 1
    while count<2000:
        #need to convert the data frames into smaller versions
        myPortfolio.sellStock('EVERYTHING')
        myPortfolio.printTotalEarnings()
        time.sleep(3)
        
        for attr in dirDfArr:
            fileName = attr[0]
            df = attr[1]
            newdf = df.iloc[-(60+count):-count]
            newdf.to_csv(f'backtestingData/{fileName}')

        tradingAlgo.main([myPortfolio])
        count+=1
        print('bought another round of stocks')

if __name__ == '__main__':
    runBackTesting()


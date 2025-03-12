import tradingAlgo.generateAnalytics as ga
import pandas as pd

if __name__ == '__main__':
    testRawdf = pd.read_csv('sp500/AAPL.csv')


    testOutputDF = ga.main(testRawdf)
    print(testOutputDF)





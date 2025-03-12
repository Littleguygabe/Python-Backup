import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    #capm formula --> ri = rf + Bi(rm-rf)
    # ri - expected return of asset
    # rf - risk free rate of return
    # Bi - beta between the stock and the market --> go over the formula for this
    # rm - the average return you expect from the entire market -- ie return of market index
    # rf - ??

    # aggressive stock -- more volatile -- beta greater than 1
    # calmer stock is beta less than 1 -- i think??
        
    market = pd.read_csv('SPX.csv',parse_dates=True,index_col='Date')

    beta = 1.2
    rfr = 0.015

    expectedReturn =  rfr + beta * ((market['Adj Close'].pct_change().mean() *252)-rfr)
    print(f'expected return --> {expectedReturn}')

if __name__ == '__main__':
    main()
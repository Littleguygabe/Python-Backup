import pandas as pd
import numpy as np

def main():
    stockFile = pd.read_csv('NVDA.csv')
    print(stockFile.loc[2516,'Open'])    

if __name__ == '__main__':
    main()
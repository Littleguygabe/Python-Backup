# neural network to indentify peaks within stock data
import pandas as pd
import os


def getSingleDataFrame():
    foldername = 'indicatorsTrainingData'
    trainingDf = pd.DataFrame()


    for file in os.listdir(foldername):
        trainingDf = pd.concat([trainingDf,pd.read_csv(f'{foldername}/{file}')])

    return trainingDf

def main():
    trainingDf = getSingleDataFrame()
    print(trainingDf)


if __name__ == '__main__':
    main()
import pandas as pd
from tensorflow import keras
import numpy as np

import matplotlib.pyplot as plt

def main():
    testIndicatorDf = pd.read_csv('indicatorsTrainingData/AAPL.csv')
    print(testIndicatorDf['isPeakIndicator'].value_counts())
    
    model = keras.models.load_model('model_checkpoint.keras')
    predictionDf = model.predict(testIndicatorDf.drop(columns=['isPeakIndicator','Close/Last']))

    #binaryPredictions = pd.DataFrame(np.where(predictionDf>0.5,1,0))
    binaryPredictions = pd.DataFrame(predictionDf)
    print(binaryPredictions.iloc[:,0])

    plt.scatter(binaryPredictions.index,binaryPredictions.iloc[:,0])
    plt.show()

if __name__ == '__main__':
    main()
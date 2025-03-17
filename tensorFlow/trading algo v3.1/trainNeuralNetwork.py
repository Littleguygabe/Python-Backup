# neural network to indentify peaks within stock data
import pandas as pd
import os

from sklearn.model_selection import train_test_split
from tensorflow import keras
from keras import Sequential,layers
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt

def trainNeuralNetwork(trainingDf):
    dropOutRate = 0.3
    val_lossList = []
    train_lossList = []

    plt.rc('figure', autolayout=True)
    plt.rc('axes', labelweight='bold', labelsize='large',
        titleweight='bold', titlesize=18, titlepad=10)
    plt.rc('animation', html='html5')
    
    scaler = StandardScaler()

    model = Sequential([
        layers.Dense(64,input_shape=(11,),activation='relu'),
        
        layers.Dense(128,activation='relu'),
        layers.Dropout(rate=dropOutRate),

        layers.Dense(256,activation='relu'),
        layers.Dropout(rate=dropOutRate),

        layers.Dense(512,activation='relu'),
        layers.Dropout(rate=dropOutRate),

        layers.Dense(512,activation='relu'),
        layers.Dropout(rate=dropOutRate),

        layers.Dense(256,activation='relu'),
        layers.Dropout(rate=dropOutRate),

        layers.Dense(1,activation='sigmoid')
    ])    

    optimiser = keras.optimizers.Adam(learning_rate = 0.1)

    model.compile(
        optimizer=optimiser,
        loss = 'binary_crossentropy',
        metrics = ['accuracy']
    )

    earlyStopping = keras.callbacks.EarlyStopping(
        monitor = 'val_loss',
        patience = 20,
        min_delta = 0.01,
        restore_best_weights = True,
    )

    reduce_lr = keras.callbacks.ReduceLROnPlateau(
        monitor = 'val_loss',
        factor = 0.5,
        patience = 5,
        min_lr = 1e-6,
    )

    checkpoint_callback = keras.callbacks.ModelCheckpoint(
        'model_checkpoint.keras',
        save_best_only = True,
        monitor = 'val_loss',
        mode='min',
        verbose=1,
    )

    X = trainingDf.drop(columns=['Close/Last','isPeakIndicator'])
    y = trainingDf['isPeakIndicator']

    Xtrain,Xtest,ytrain,ytest = train_test_split(X,y,test_size=0.3,random_state=42)

    history = model.fit(
        Xtrain,ytrain,
        validation_data=(Xtest,ytest),
        batch_size = 64,
        epochs=750, 
        callbacks=[reduce_lr,checkpoint_callback],
        #verbose=0,
    )

    historyDf = pd.DataFrame(history.history)
    val_lossList.append(historyDf['val_loss'].iloc[-1])
    train_lossList.append(historyDf['loss'].iloc[-1])

    historyDf.loc[:,['loss','val_loss']].plot()

    plt.show()

def getSingleDataFrame():
    foldername = 'indicatorsTrainingData'
    trainingDf = pd.DataFrame()


    for file in os.listdir(foldername):
        trainingDf = pd.concat([trainingDf,pd.read_csv(f'{foldername}/{file}')])

    trainingDf = trainingDf.reset_index(drop=True)

    return trainingDf

def main():
    trainingDf = getSingleDataFrame()

    trainNeuralNetwork(trainingDf)

if __name__ == '__main__':
    main()
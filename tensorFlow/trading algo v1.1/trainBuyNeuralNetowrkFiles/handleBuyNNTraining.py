from sklearn.model_selection import train_test_split
from tensorflow import keras
from keras import Sequential,layers
from sklearn.preprocessing import StandardScaler
import joblib
import time
import os
import dataRead
import pandas as pd

import matplotlib.pyplot as plt

def trainNeuralNetwork():
    dropoutRate = 0.3
    learningRate = 0.001
    batchSize = 512
    Nepochs = 750
    testSize = 0.3
    trainingFolder = 'nasdaq100'

    trainingData = dataRead.retrieveData([trainingFolder])

    scaler = StandardScaler()

    model = Sequential([
        layers.InputLayer(input_shape=(7,)),

        layers.Dense(128,activation='leaky_relu'),
        layers.Dropout(rate=dropoutRate),
        
        layers.Dense(256,activation='leaky_relu'),
        layers.Dropout(rate=dropoutRate),
        
        #layers.Dense(512,activation='leaky_relu'),
        #layers.Dropout(rate=dropoutRate),

        layers.Dense(256,activation='leaky_relu'),
        layers.Dropout(rate=dropoutRate),

        layers.Dense(256,activation='leaky_relu'),
        layers.Dropout(rate=dropoutRate),  

        layers.Dense(128,activation='leaky_relu'),
        layers.Dropout(rate=dropoutRate),
        #doubled the number of neurons in the last 2 layers
        #added a new layer of 128 neurons

        layers.Dense(100,activation='softmax')
        ])

    optimiser = keras.optimizers.Adam(learning_rate=learningRate)

    model.compile(
        optimizer=optimiser,
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )


    earlyStopping = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=20,
        min_delta=0.01,
        restore_best_weights=True
    )

    reduce_lr = keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6
    )


    checkpoint_callback = keras.callbacks.ModelCheckpoint(
        'model_checkpoint.keras', 
        save_best_only=True,  # Save the best model based on validation loss
        monitor='val_loss',  # Monitor the validation loss
        mode='min',  # Minimize the loss
        verbose=1

    )

    count = 0
    totalvalAcc = 0
    trainingData = trainingData.dropna()
    trainingData['riskLevel'] = trainingData['riskLevel'].round().astype(int)


        # One-hot encode labels
    y = keras.utils.to_categorical(trainingData['riskLevel'] - 1, num_classes=100)

    X = trainingData.drop(columns=['riskLevel','Date'], axis=1)

    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=testSize, random_state=42)


    Xtrain = scaler.fit_transform(Xtrain)
    Xtest = scaler.transform(Xtest)

    history = model.fit(
            Xtrain, ytrain,
            validation_data=(Xtest,ytest),
            batch_size=batchSize,
            epochs=Nepochs,
            callbacks=[reduce_lr,checkpoint_callback,earlyStopping],
            verbose=1
            #changed the number of epochs to 500
    )    

    count+=1
    totalvalAcc += history.history['val_accuracy'][-1]
    print(history.history['val_accuracy'][-1])

    plt.plot(history.history['accuracy'], label ='training accuracy')
    plt.plot(history.history['val_accuracy'],label='validation accuracy')
    plt.legend()
    plt.show()

    model.save('trainBuyNeuralNetowrkFiles/buyNNmodel.keras')

    joblib.dump(scaler,'trainBuyNeuralNetowrkFiles/buyScaler.pkl')
    print(f'average val_accuracy: {totalvalAcc/count}')


trainNeuralNetwork()

#change the standardisation so that it doesnt form in a bell curve 
#   -> z-score standardisation -- mean 0 standard variation 1
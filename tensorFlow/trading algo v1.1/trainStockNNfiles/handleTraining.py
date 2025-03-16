from dataRead import *
from sklearn.model_selection import train_test_split
from tensorflow import keras
from keras import Sequential,layers
from sklearn.preprocessing import StandardScaler
import time
import os

from storeAnalytics import *


import matplotlib.pyplot as plt

def trainNeuralNetwork(learningParameters):
    dropoutRate = learningParameters[0]
    learningRate = learningParameters[1]
    batchSize = learningParameters[2]
    Nepochs = learningParameters[3]
    testSize = learningParameters[4]
    trainingFolder = learningParameters[5]
    graphDataBool = learningParameters[7]
    isTest = learningParameters[8]
    

    plt.rc('figure', autolayout=True)
    plt.rc('axes', labelweight='bold', labelsize='large',
        titleweight='bold', titlesize=18, titlepad=10)
    plt.rc('animation', html='html5')

    #this model uses binary classification rather than trying to predict the close price of the stock
    #so basically just says whether to buy the stock or not rather than giving accurate predictions on how much it will change
    # so the simpler model of the 2 that are being created

    csvFileList = os.listdir(trainingFolder)

    dataFrameList = []
    trainTestLossPercentageDifList = []
    val_lossList = []
    train_lossList = []

    for file in csvFileList:
        dataFrameList.append(main(file,trainingFolder))


    scaler = StandardScaler()

    model = Sequential([
        layers.BatchNormalization(input_shape=(16,)),

        layers.Dense(128,activation='leaky_relu'),
        layers.BatchNormalization(),
        layers.Dropout(rate=dropoutRate),
        
        layers.Dense(256,activation='leaky_relu'),
        layers.BatchNormalization(),
        layers.Dropout(rate=dropoutRate),
        
        layers.Dense(512,activation='leaky_relu'),
        layers.BatchNormalization(),
        layers.Dropout(rate=dropoutRate),

        layers.Dense(512,activation='leaky_relu'),
        layers.BatchNormalization(),
        layers.Dropout(rate=dropoutRate),

        layers.Dense(256,activation='leaky_relu'),
        layers.BatchNormalization(),
        layers.Dropout(rate=dropoutRate),  

        layers.Dense(128,activation='leaky_relu'),
        layers.BatchNormalization(),
        layers.Dropout(rate=dropoutRate),
        #doubled the number of neurons in the last 2 layers
        #added a new layer of 128 neurons

        layers.Dense(3,activation='linear')
        ])

    optimiser = keras.optimizers.Adam(learning_rate=learningRate)

    model.compile(
        optimizer=optimiser,
        loss='mse',
        metrics=['mae']
    )


    earlyStopping = keras.callbacks.EarlyStopping(
        monitor='val_mae',
        patience=20,
        min_delta=0.01,
        restore_best_weights=True
    )

    reduce_lr = keras.callbacks.ReduceLROnPlateau(
        monitor='val_mae', factor=0.5, patience=5, min_lr=1e-6
    )


    checkpoint_callback = keras.callbacks.ModelCheckpoint(
        'model_checkpoint.keras', 
        save_best_only=True,  # Save the best model based on validation loss
        monitor='val_mae',  # Monitor the validation loss
        mode='min',  # Minimize the loss
        verbose=1

    )

    count = 0

    startTime = time.time()


    for dataframe in dataFrameList:
        dsStartTime = time.time()
        print('current data file: ',csvFileList[count]) 

        X = dataframe.drop(columns=['Date','3DayPercentageChange','5DayPercentageChange','10DayPercentageChange'])
        y = dataframe[['3DayPercentageChange','5DayPercentageChange','10DayPercentageChange']]


    #Partition data
        Xtrain,Xtest,ytrain,ytest = train_test_split(X,y,test_size=testSize,random_state=42)

        Xtrain = scaler.fit_transform(Xtrain)
        Xtest = scaler.transform(Xtest)


        history = model.fit(
            Xtrain, ytrain,
            validation_data=(Xtest,ytest),
            batch_size=batchSize,
            epochs=Nepochs,
            callbacks=[reduce_lr,checkpoint_callback,earlyStopping],
            verbose=0
            #changed the number of epochs to 500
        )    

        history_df = pd.DataFrame(history.history)
        val_lossList.append(history_df['val_mae'].iloc[-1])
        train_lossList.append(history_df['mae'].iloc[-1])
        
        #to show the learning on a graph
        if graphDataBool:    
            #history_df.loc[:,['loss','val_loss']].plot(title=f'Cross-Entropy Loss for {csvFileList[count]}')
            history_df.loc[:,['mae','val_mae']].plot(title=f'MAE for {csvFileList[count]}')
        
        trainTime = time.time()-dsStartTime
        print(f'Time taken to learn last dataset: {trainTime//60}m {trainTime%60}s')

        if earlyStopping.stopped_epoch:
            timeForFullEpochSize = trainTime*(Nepochs/earlyStopping.stopped_epoch)

        else:
            timeForFullEpochSize = trainTime

        maxTrainTime = timeForFullEpochSize*(len(dataFrameList)-(count+1))
        print(f'Max potential training time: {maxTrainTime//3600}h:{maxTrainTime%3600//60}m:{maxTrainTime%60}s')

        count+=1



    for trainLoss,valLoss in zip(train_lossList,val_lossList):
        trainTestLossPercentageDifList.append(((valLoss-trainLoss)/trainLoss)*100)


    if learningParameters[6]:
        modelVersion = getNextModelVersion()

        if isTest:
            modelVersion = str(modelVersion)+'_test'

        model.save(f'models/model_{modelVersion}.keras')

        stockDataArray = [csvFileList,modelVersion,val_lossList,trainTestLossPercentageDifList]
        storeStockData(stockDataArray)
        modelDataArray = [modelVersion,dropoutRate,learningRate,batchSize,Nepochs,testSize,csvFileList,val_lossList,(time.time()-startTime),trainTestLossPercentageDifList,model,trainingFolder]
        storeModelData(modelDataArray)


    if graphDataBool:
        plt.show()
    #want to take all the data being printed and place it into a data frame to then write to a csv File
    #have one csv file to hold the data from the stock analysis -> mae loss and everything
    #have another csv file to represent the hyper parameters used for the model and then also the average mae val_loss for the parameters


    #data being used: trainLoss,valLoss,trainTestLossPercentageDifList, time.time() and start time, csvFileList

import trainStockNNfiles.handleTraining as handleTraining

#network parameters
dropoutRate = 0.1
learningRate = 0.001
batchSize = 384
Nepochs = 750
percentageOfDataUsedForTesting = 0.2

#data parameters
dataTrainingFolder = 'smallTestSet'
saveModel = False
graphData = False
isTest = False

handleTraining.trainNeuralNetwork([dropoutRate,learningRate,batchSize,Nepochs,percentageOfDataUsedForTesting,dataTrainingFolder,saveModel,graphData,isTest])

#need to plot the predictions for a given stock

#could be a good idea to add directional indicators to see the direction of the current trend
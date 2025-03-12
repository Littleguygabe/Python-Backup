import trainBuyNeuralNetowrkFiles.dataRead as dataRead
import matplotlib.pyplot as plt

df = dataRead.retrieveData(['debugData'])

print(df)

plt.hist(df['riskLevel'])

plt.show()


#need to change the data so that it is percenatge scaled within the stock rather than the data base as a whole
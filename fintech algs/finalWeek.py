import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def main():
    #can approximate the return from stocks using the normal distribution
    #would be better off using T distribution as normal distribution doesnt take into account the No outliers that occur
    #in financial markets

    #analyst role application on the fintech insta link tree

    #finish the last few jupiter notebooks then submit for the certification

    apple = pd.read_csv('TSLA.csv')
    apple.set_index('Date',inplace=True)

    apple['return'] = apple['Close'].pct_change()
    apple['MA40'] = apple['Close'].rolling(window=40).mean()
    apple['MA200'] = apple['Close'].rolling(window=200).mean()

    apple['return_next_day'] = apple['return'].shift(-1) # moves the returns up a day so we can use it as training data

    apple.dropna(subset=['MA40','MA200','return_next_day'],inplace=True)

    x = apple[['MA40','MA200']]
    y = apple['return_next_day']

    xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size=0.2,random_state=42)
    model = LinearRegression()
    model.fit(xtrain,ytrain)

    apple['predReturn'] = model.predict(x)
    apple['signal'] = np.where(apple['predReturn']>0,1,-1)

    apple['stratreturn'] = apple['signal'].shift(1)*apple['return']
    apple['cumulativeStratReturn'] = (1+apple['stratreturn']).cumprod()
    apple['cumulativeMarketReturn'] = (1+apple['return']).cumprod()

    #apple['predPercentageReturn'] = (apple['predReturn']*10000)


    print(apple)

    #plt.plot(apple['predPercentageReturn'],label='percentage return from prediction')

    plt.plot(apple['cumulativeStratReturn'],label='Strat Return')
    plt.plot(apple['cumulativeMarketReturn'],label='Market Return')



    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
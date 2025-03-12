import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

#need to create own jupiter notebook to analyse a stock -> then send to them to get certificate

def main():
    die = pd.DataFrame([1,2,3,4,5,6])

    trial = 50

    result = [die.sample(2, replace=True).sum().loc[0] for i in range(trial)]
    
    freq = pd.DataFrame(result)[0].value_counts()
    sort_freq = freq.sort_index()

    sort_freq.plot(kind='bar',color='blue')

if __name__ == '__main__':
    main()
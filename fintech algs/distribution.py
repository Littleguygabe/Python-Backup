import pandas as pd
import numpy as np

def main():
    die = pd.DataFrame(np.arange(1,6))
    dieSum = die.sample(2,replace=True).sum().loc[0] 

    print(dieSum)   

if __name__ == '__main__':
    main()
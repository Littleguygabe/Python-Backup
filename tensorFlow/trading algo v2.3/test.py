import os 
import pandas as pd
total = 0
for file in os.listdir('sp500'):
    total+=len(pd.read_csv(f'sp500/{file}'))


print(total)
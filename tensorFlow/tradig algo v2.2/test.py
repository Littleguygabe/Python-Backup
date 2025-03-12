import os
import pandas as pd

foldername = 'nasdaq100'

fileList = os.listdir(foldername)
for file in fileList:
    tempdf = pd.read_csv(f'{foldername}/{file}')
    if len(tempdf)<2000:
        print(f'{file} is undersized with size: {len(tempdf)}')
        #os.remove(f'{foldername}/{file}')
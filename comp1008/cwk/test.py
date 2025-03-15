import pandas as pd
df = pd.read_csv('winequality-red.csv')
dfDropped = df.dropna()
print(dfDropped)


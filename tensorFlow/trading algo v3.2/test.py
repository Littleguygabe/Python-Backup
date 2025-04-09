import pandas as pd
df = pd.read_csv('analysisFiles/1.csv')

for col in df.columns:
    print(col)
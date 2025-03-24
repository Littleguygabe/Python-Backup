import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('winequality-red.csv') 


correlation_matrix = df.corr()
plt.figure(figsize=(12,10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.show()


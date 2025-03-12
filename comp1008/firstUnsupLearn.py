import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans

iris = load_iris()
data = pd.DataFrame(iris.data, columns=iris.feature_names)

# ^^ Data pre-processing

#training the K cluster model
x=data.values
kmeans = KMeans(n_clusters=3, max_iter = 100,random_state=0)
y_kmeans = kmeans.fit_predict(x)

#visualizing the clusters
plt.scatter(x[y_kmeans == 0, 0], x[y_kmeans == 0, 1], s = 50, c = 'red', label = 'c1',marker='x')
plt.scatter(x[y_kmeans == 1, 0], x[y_kmeans == 1, 1], s = 50, c = 'blue', label = 'c2',marker='x')
plt.scatter(x[y_kmeans == 2, 0], x[y_kmeans == 2, 1], s = 50, c = 'green', label = 'c3',marker='x')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s = 100, c = 'black', label = 'Centroids',marker='x')
plt.legend()
plt.show()


""" 
plt.scatter(data['sepal length (cm)'], data['sepal width (cm)'],marker='x')
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.show() """



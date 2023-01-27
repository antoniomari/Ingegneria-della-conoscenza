import pandas as pd
import sys
from my_embedding import WebDataPickUp
from my_embedding import Embedding
import nltk
from sklearn.cluster import KMeans
import matplotlib
import seaborn
import numpy

def create_embedding():

    nltk.download('punkt')
    df = pd.read_csv("embeddings.csv")
    wcss = []
    my_embedding = df.to_numpy().tolist()
    print(type(my_embedding))

    # Trying to get best number of clusters
    for i in range(1, 3):
        clustering = KMeans(n_clusters = i, init = 'k-means++', random_state = 100)
        clustering.fit(my_embedding)
        wcss.append(clustering.inertia_)

    ks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    print(ks, wcss)
    matplotlib.pyplot.plot(ks, wcss)
    matplotlib.pyplot.show()

    pass
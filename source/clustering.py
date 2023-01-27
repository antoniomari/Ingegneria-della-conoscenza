import pandas as pd
import sys
from my_embedding import WebDataPickUp
from my_embedding import Embedding
import nltk
from sklearn.cluster import KMeans
import matplotlib
import seaborn
import numpy
from sklearn.preprocessing import normalize

def make_clusters():

    nltk.download('punkt')
    df = pd.read_csv("embeddings.csv")

    # normalize embeddings
    victim_codes = df["VICTIM_CODE"]
    df = pd.DataFrame(normalize(df.drop(["VICTIM_CODE"], axis=1), axis=1))
    df = df.assign(VICTIM_CODE=victim_codes)
    # save normalized
    df.to_csv("normalized_embeddings.csv", index=False)

    wcss = []
    my_embedding = df.drop(["VICTIM_CODE"], axis=1).to_numpy().tolist()

    # Trying to get best number of clusters
    for i in range(1, 21):
        clustering = KMeans(n_clusters = i, init = 'k-means++', random_state = 100, n_init=10)
        clustering.fit(my_embedding)
        wcss.append(clustering.inertia_)

    ks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    print(ks, wcss)
    matplotlib.pyplot.xticks(ks)
    matplotlib.pyplot.plot(ks, wcss)
    matplotlib.pyplot.show()

    pass

make_clusters()
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
    df = pd.read_csv("shoot_selected.csv")
    names = df[df["VICTIMIZATION"] == 'homicide'] [['HOMICIDE_VICTIM_FIRST_NAME', 'HOMICIDE_VICTIM_LAST_NAME']]
    articles = [['this', 'is', 'my', 'test'], ['please', 'another'], ['look', 'here'], ['hello', 'to', 'everyone'], ['satantango', 'by', 'Bela', 'Tarr'], ['']]
    print(names[names['HOMICIDE_VICTIM_FIRST_NAME'] == 'nan'])

    for index, row in names.iterrows():
        try:
            query = "Chicago homicide " + row['HOMICIDE_VICTIM_FIRST_NAME'] + " " + row['HOMICIDE_VICTIM_LAST_NAME']
            news = [WebDataPickUp(query, 3).pick_up()]
            articles.append(news)
            print(news)
        except:
            pass
    print(articles)

    my_embedding = Embedding.build_embedding(articles)
    print(my_embedding)
    pd.DataFrame(my_embedding).to_csv("pandasarray.csv")
    wcss = []
    
    # Trying to get best number of clusters
    for i in range(1, 21):
        clustering = KMeans(n_clusters = i, init = 'k-means++', random_state = 100)
        clustering.fit(my_embedding)
        wcss.append(clustering.inertia_)

    ks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    print(ks, wcss)
    matplotlib.pyplot.plot(ks, wcss)
    matplotlib.pyplot.show()

    pass
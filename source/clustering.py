import pandas
import sys
from my_embedding import WebDataPickUp
from my_embedding import Embedding
import nltk
from sklearn.cluster import KMeans
import matplotlib
import seaborn

def create_embedding():

    nltk.download('punkt')
    df = pandas.read_csv("shoot_selected.csv")
    names = df[df["VICTIMIZATION"] == 'homicide'] [['HOMICIDE_VICTIM_FIRST_NAME', 'HOMICIDE_VICTIM_LAST_NAME']]
    articles = [['this', 'is', 'my', 'test'], ['this', 'another']]

    #for index, row in names.iterrows():
    #    try:
    #        query = "Chicago homicide " + row['HOMICIDE_VICTIM_FIRST_NAME'] + " " + row['HOMICIDE_VICTIM_LAST_NAME']
    #        news = [WebDataPickUp(query, 3).pick_up()]
    #        articles.append(news)
    #        print(news)
    #    except:
    #        pass
    print(articles)
    
    my_embedding = Embedding.build_embedding(articles)
    print(my_embedding)
    wcss = []

    # Trying to get best number of clusters
    for i in range(1, 10):
        clustering = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
        clustering.fit(my_embedding)
        wcss.append(clustering.inertia_)

    ks = [1,2,3,4,5,6,7,8,9,10]
    seaborn.lineplot(x = ks, y = wcss)

    pass
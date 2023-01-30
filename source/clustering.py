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
import seaborn
from sklearn.metrics import pairwise_distances
from scipy import stats
import wordcloud
from collections import deque

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
    my_embedding = df.drop(["VICTIM_CODE"], axis=1).to_numpy()

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

#make_clusters()

#After an observation, we have choosen 4 as number of clusters
def final_cluster():

    df = pd.read_csv("embeddings.csv")
    df_shoot = pd.read_csv("shoot_selected.csv")
    df_working_dataset = pd.read_csv("working_dataset.csv")
    df_arrest_dataset = pd.read_csv("arrest_selected.csv")

    my_embedding = df.drop(["VICTIM_CODE"], axis=1).to_numpy()
    n = 4
    clustering = KMeans(n_clusters = n, init = 'k-means++', random_state = 100, n_init=10)
    clustering.fit(my_embedding)

    df["Cluster"] = clustering.labels_
    #clusterdf = {str(i) : df[df["Cluster"] == i] for i in range(0, n)}

    complete_df = pd.merge(df, df_shoot, on="VICTIM_CODE")
    complete_df = pd.merge(complete_df, df_working_dataset, on="CASE_NUMBER")
    complete_df = pd.merge(complete_df, df_arrest_dataset, on="CASE_NUMBER")
    complete_df = complete_df.drop([str(i) for i in range(0, 300)], axis=1)
    complete_df = complete_df.drop("VICTIM_CODE", axis=1)

    mapping = {"api":1, "blk":2, "wbh":3, "whi":4,"wwh":5, "unknown":6}
    map_sex = {"m":1, "f":2}

    complete_df['criminal_race'] = complete_df['criminal_race'].map(mapping)
    complete_df['victim_race'] = complete_df['victim_race'].map(mapping)
    complete_df['SEX'] = complete_df['SEX'].map(map_sex)
    complete_df.to_csv("dataset_clustered.csv")
    columns = ["criminal_race", "AGE", "victim_race","NIGHT_CRIME","SEX","Cluster", "AREA", "GUNSHOT", "STATE_HOUSE_DISTRICT", "AREA_POVERTY_HEALTH", "AREA_HIGH_SCHOOL_DIPLOMA", "AREA_UNEMPLOYMENT", "AREA_BIRTH_RATE", "NUM_OF_DEAD", "IMMEDIATE_ARREST", "IS_DOMESTIC", "NUM_OF_VICTIMS"]
    complete_df = complete_df[columns]
    complete_df.dropna()

    df_statistics = []
    for i in range(0, n):
        df_statistics.append(complete_df.loc[complete_df["Cluster"] == i])
        complete_df.loc[complete_df["Cluster"] == i].describe().to_csv("Statistic" + str(i) + ".csv")
        seaborn.heatmap(df_statistics[i].corr())
        #matplotlib.pyplot.show()

    df_statistics[0] = df_statistics[0].drop(["Cluster"], axis=1)
    df_statistics[1] = df_statistics[1].drop(["Cluster"], axis=1)
    df_statistics[2] = df_statistics[2].drop(["Cluster"], axis=1)
    df_statistics[3] = df_statistics[3].drop(["Cluster"], axis=1)

    columns.remove("Cluster")

    for col in columns:
        f, p = stats.f_oneway(df_statistics[0][col].values, df_statistics[1][col].values,df_statistics[2][col].values, df_statistics[3][col].values)
        if p < 0.05: # hp
            print("Different data for column:", col, "values are ", format(f), format(p))
        else:
            print("Not much different data for column:", col, "values are ", format(f), format(p))

def create_wordcloud():
    df = pd.read_csv("dataset_clustered.csv")
    news = [''] * 4

    for index, row in df.iterrows():
        print("News of cluster (",row['Cluster'],")")
        news[int(row["Cluster"])] += WebDataPickUp(row["HOMICIDE_VICTIM_FIRST_NAME"] + row["HOMICIDE_VICTIM_LAST_NAME"] + " Chicago homicide", 3).pick_up()

    for i in range(0, 4):
        wc = wordcloud.WordCloud(stopwords=set(wordcloud.STOPWORDS)).generate(news[i])
        matplotlib.pyplot.imshow(wc)
        matplotlib.pyplot.axis('off')
        matplotlib.pyplot.show()
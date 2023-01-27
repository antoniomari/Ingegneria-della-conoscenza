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
    articles = []

    for index, row in df.iterrows():

        if pd.isnull(row["HOMICIDE_VICTIM_FIRST_NAME"]):
            continue

        try:
            query = "Chicago homicide " + row['HOMICIDE_VICTIM_FIRST_NAME'] + " " + row['HOMICIDE_VICTIM_LAST_NAME']
            news = WebDataPickUp(query, 3).pick_up()
            articles.append(news.split())
            print(articles)

        except: pass
        embedding = Embedding.build_embedding(articles)
        print(embedding)
        embedding_df: pd.DataFrame = pd.DataFrame(embedding)
        embedding_df["VICTIM_CODE"] = row["VICTIM_CODE"]
        embedding_df.to_csv("embeddings.csv", mode='a', index=False, header=False)

        articles = []

create_embedding()
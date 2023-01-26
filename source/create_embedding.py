import pandas
import pandas as pd
from my_embedding import WebDataPickUp
from my_embedding import Embedding
import nltk


def create_embedding():
    nltk.download('punkt')
    df = pandas.read_csv("shoot_selected.csv")
    articles = []
    count = 0

    for index, row in df.iterrows():

        if pd.isnull(row["HOMICIDE_VICTIM_FIRST_NAME"]):
            continue

        #try:
        query = "Chicago homicide " + row['HOMICIDE_VICTIM_FIRST_NAME'] + " " + row['HOMICIDE_VICTIM_LAST_NAME']
        news = [WebDataPickUp(query, 3).pick_up()]
        articles.append(news)
        print(news)
        #except:

        embedding_df: pd.DataFrame = pd.DataFrame(Embedding.build_embedding(articles))
        embedding_df["VICTIM_CODE"] = row["VICTIM_CODE"]
        embedding_df.to_csv("embeddings.csv", mode='a', index=False)

        articles = []

        count += 1


create_embedding()

import pandas as pd
import numpy as np
import newspaper
import nltk
import gensim as gs
import googlesearch
from gensim import corpora
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
import gensim.downloader as api

class Embedding:

    def build_embedding(original_sentences):

            MAX_WORDS = 25000
            MAX_SEQUENCE_LENGTH = 80

            tokenizer = Tokenizer(num_words=MAX_WORDS, char_level=False)
            tokenizer.fit_on_texts(original_sentences)

            sequences = tokenizer.texts_to_sequences(original_sentences)

            word_index = tokenizer.word_index
            #print('Found %s unique tokens.' % len(word_index))

            #print("First: ",sequences[0])
            #print("Second: ",sequences[1])
            #print(type(tokenizer.word_index), len(tokenizer.word_index))
            index_to_word = dict((i, w) for w, i in tokenizer.word_index.items())
            #print(" ".join([index_to_word[i] for i in sequences[0]]))
            #print(" ".join([index_to_word[i] for i in sequences[1]]))

            # Pad our sequences to fixed size (only for deep learning model)
            padded_sequences = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH, padding='post')
            #print(padded_sequences)

            word2vec_model300 = api.load('word2vec-google-news-300')

            news = []

            for sentence in padded_sequences:
                # Our size will be 300
                sum_emb = [0 for k in range(300)] 
                num_tok = 0
                this_news = []
                for tok in sentence:
                    if tok != 0:
                        word = list(word_index.keys())[list(word_index.values()).index(tok)]
                        try:
                            word_embedding = word2vec_model300[word]
                            #Sum embeddings
                            sum_emb = [x + y for x, y in zip(sum_emb, word_embedding)]
                            num_tok = num_tok + 1
                        except: # skip
                            pass
                if num_tok != 0: # I found at least a word
                    this_news = [ x / num_tok for x in sum_emb]

                # Add last news in collection
                news.append(this_news)

            news = np.array(news)
            #print(news)
            return news
            pass

class WebDataPickUp:

    def __init__(self, query, n_istances):
        self.m_query = query
        self.m_nistances = n_istances

    def pick_up(self):
        result = ""
        for x in googlesearch.search(self.m_query, stop = self.m_nistances):
            try:
                art = newspaper.Article(x)
                art.download()
                art.parse()
                art.nlp()
                result += art.title + art.text
            except:
                pass
        return result

# Example of usage. Note that this is a list of lists
#print(Embedding.build_embedding([['this', 'is', 'my', 'test'], ['this', 'another']]))


a = [['this is my test'], ['this another']]

a = [sentence[0].split("\\s") for sentence in a]
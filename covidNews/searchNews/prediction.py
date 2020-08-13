import joblib
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.tokenize import sent_tokenize
from nltk.tokenize import TreebankWordTokenizer 
from nltk.tokenize import RegexpTokenizer 
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
'''predict the sentiments of all the seeded data'''

from nltk import pos_tag
import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
from model import tfidf as tfidf
import csv
import os
from elasticsearch import Elasticsearch


def predict_sentiment(data, es):
    if data['hits']['hits'] == []:
        print('empty list')
        return 
    dic_articles = {'Id':[],
                    'Description':[],
                    'Content':[], 
                    'PublishedAt':[]
                    }
    # create a dataframe fro each date and description 
    for article in data['hits']['hits']: 
        dic_articles['Id'].append(article['_id'])
        dic_articles['Description'].append(article['_source']['description'])
        dic_articles['Content'].append(article['_source']['content'])
        dic_articles['PublishedAt'].append(article['_source']['publishedAt'])

    df = pd.DataFrame.from_dict(dic_articles)
    df_x = df['Content']


    # We transform each text into a vector
    features = tfidf.transform(df_x.astype('U')).toarray()

    filename = 'finalized_model.sav'
    loaded_model = joblib.load(filename)
    df_y = loaded_model.predict(features)

    # print(df_x[9], df['Id'][9], df['PublishedAt'][9], df['Description'][9], df_y[9])

    # create an index
    if not es.indices.exists(index="news-sentiment"):
        es.indices.create(index='news-sentiment', ignore=400) 

    dic_sentiments={}
    # add articles to the Elasticsearch index
    for i in range(0, len(df_x)):
        try:
            # create a dic of new data with sentiment
            dic_sentiments['description'] = df['Description'][i]
            dic_sentiments['content'] = df_x[i]
            dic_sentiments['publishedAt'] = df['PublishedAt'][i]
            dic_sentiments['sentiment'] = df_y[i]

            # add to elasticsearch
            article = es.index(index='news-sentiment', id=df['Id'][i], body=dic_sentiments)
        except:
            continue


    # query = {"size": 1000,"query":{"match_all" : {}}}
    # data = es.search(index="news-sentiment", body=query)
    # print("\n\n\n", data)

if __name__ == "__main__":
    # loading data
    ip=os.environ.get('IP')

    # connect to elasticsearch
    es=Elasticsearch(["http://"+ip])
    query = {"size": 1000,"query":{"match_all" : {}}}
    data = es.search(index="news-articles", body=query)
    predict_sentiment(data, es)




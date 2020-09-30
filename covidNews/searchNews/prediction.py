'''Sentiment Analysis of News Data'''

import joblib
import pandas as pd 
from model import tfidf as tfidf
import csv
import os
from elasticsearch import Elasticsearch
from datetime import datetime
import pickle
 
def predict_sentiment(data, es):
    
    if data['hits']['hits'] == []:
        print('empty list')
        return 
    
    dic_articles = {'Id':[],
                    'Description':[],
                    'Content':[], 
                    'PublishedAt':[]
                    }
    
    # create a dataframe for each date and description 
    for article in data['hits']['hits']: 
        dic_articles['Id'].append(article['_id'])
        dic_articles['Description'].append(article['_source']['description'])
        dic_articles['Content'].append(article['_source']['content'])
        dic_articles['PublishedAt'].append(article['_source']['publishedAt'])

    df = pd.DataFrame.from_dict(dic_articles)
    df_x = df['Description']

    tfidf = pickle.load(open("tfidf2.pk", "rb"))

    # Create new tfidfVectorizer with old vocabulary
    tf_new = TfidfVectorizer(sublinear_tf=True, min_df=5,
                          ngram_range=(1, 2), 
                          stop_words='english',
                          vocabulary = tfidf.vocabulary_)

    # We transform each text into a vector
    features = tf_new.fit_transform(df_x.astype('U')).toarray()

    filename = 'finalized_model.sav'
    loaded_model = joblib.load(filename)
    df_y = loaded_model.predict(features)

    # create an index
    if not es.indices.exists(index='news-sentiment'):
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

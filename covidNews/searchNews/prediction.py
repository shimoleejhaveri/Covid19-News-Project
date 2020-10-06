'''Sentiment Analysis of News Data'''

import csv
import os
import joblib
import pandas as pd 
from elasticsearch import Elasticsearch
from datetime import datetime
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
 
def predict_sentiment(data, es):
    
    if data['hits']['hits'] == []:
        print('Elasticsearch is empty')
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

    # get the tfidf.pk
    tfidf = pickle.load(open("tfidf.pk", "rb"))

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

    dic_sentiments={}

    for i in range(0, len(df_x)):
        try:
            # create a dic of new data with sentiment
            dic_sentiments['description'] = df_x[i]
            dic_sentiments['content'] = df['Content'][i]
            dic_sentiments['publishedAt'] = df['PublishedAt'][i]
            dic_sentiments['sentiment'] = df_y[i]

            res = es.get(index="news-articles3", id=df['Id'][i])

            dic_article_by_id = res['_source']
            if dic_article_by_id:
                dic_article_by_id['sentiment'] = df_y[i]

                # update elasticsearch with the sentiment
                response = es.index(index="news-articles3", id=df['Id'][i], body=dic_article_by_id)

        except:
            continue




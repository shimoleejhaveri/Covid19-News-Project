'''Covid News'''

import os
from elasticsearch import Elasticsearch
import requests
import json
from pytz import timezone
import datetime

key=os.environ.get('API_KEY')
ip=os.environ.get('IP')
es = Elasticsearch(["http://"+ip])

def dailySentAnalysis():

    query = {"size": 1000,"query":{"match_all" : {}}}
    data = es.search(index="news-sentiment", body=query)
 
    if data['hits']['hits'] == []:
        return 0

    articles = {}

    for article in data['hits']['hits']: 
        key = article['_source']['publishedAt']
        sent = article['_source']['sentiment']

        def add(key, articles, sent):
            if key in articles:
                articles[key][sent] += 1
            else:
                articles[key] = {'positive':0, 'neutral':0, 'negative':0}
                articles[key][sent] += 1

            return articles
   
        if sent == 1 :
            add(key, articles, 'negative')
        if sent == 2 :
            add(key, articles, 'positive')
        if sent == 0 :
            add(key, articles, 'neutral')


    return articles

def sentAnalysis():

    query = {"size": 1000,"query":{"match_all" : {}}}
    data = es.search(index="news-sentiment", body=query)
 
    if data['hits']['hits'] == []:
        return 0

    neutral = []    
    positive = []
    negative = []

    # create a dictionary of articles and sentiments 
    for article in data['hits']['hits']: 
        try:
            if article['_source']['sentiment'] == 0:
                article = {'description':article['_source']['description'],
                            'publishedAt':article['_source']['publishedAt']
                }
                neutral.append(article)

            if article['_source']['sentiment'] == 1:
                article = {'description':article['_source']['description'],
                            'publishedAt':article['_source']['publishedAt']
                }
                negative.append(article)

            if article['_source']['sentiment'] == 2:
                article = {'description':article['_source']['description'],
                            'publishedAt':article['_source']['publishedAt']
                }
                positive.append(article)
        except:
            continue
      
    return {'positive': len(positive), 'negative': len(negative), 'neutral': len(neutral)}

def displayNews():

    tz = timezone("US/Pacific")
    today = str(datetime.datetime.now(tz))[:10]

    payload = {"q": "Covid-19", 
                "from": today, 
                "sortBy": "publishedAt", 
                "language": "en",
                "apiKey": key}

    url = requests.get("http://newsapi.org/v2/top-headlines", params=payload).json()
  
    articles = url["articles"]
    article_list = []
      
    for article in articles:

        article_dict = {'source': article["source"],
                        'title': article["title"],
                        'description': article["description"],
                        'url': article["url"],
                        'url_img': article["urlToImage"],
                        'publication_date': article["publishedAt"][:10]}
          
        article_list.append(article_dict)
    return article_list
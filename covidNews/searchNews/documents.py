'''Covid-19 News Landing Page'''

import os
from elasticsearch import Elasticsearch
import requests
import json
from pytz import timezone
import datetime

key = os.environ.get('API_KEY')
ip = os.environ.get('IP')

es = Elasticsearch(['http://' + ip])

def display_news(es):

    query = {'size': 1000, 'sort' : [{'publishedAt' : {'order' : 'desc'}}]}
    
    data = es.search(index="news-articles", body=query)
    articles = data['hits']['hits']
   
    article_list = []
    list_words = ['covid-19', 'covid19' 'virus', 'coronavirus', \
    'pandemic', 'sars', 'sars-cov-2', 'endemic', 'epidemic', 'quarantine', \
    'vaccine', 'asymptomatic', 'incubation', 'spread', 'containment',\
     'pneumonia', 'disease']

    for article in articles:
        new_article = article['_source']
        
        if any(word in (new_article['title']).lower() for word in list_words):
            article_dict = {'source': new_article['source_name'],
                            'title': new_article['title'],
                            'description': new_article['description'],
                            'url': new_article['url'],
                            'publication_date': new_article['publishedAt'][:10]}
                  
            article_list.append(article_dict)
        
    return article_list[:17]

def daily_sent_analysis():

    query = {'size': 1000, 'query':{'match_all' : {}}}
    data = es.search(index='news-articles', body=query)
 
    if data['hits']['hits'] == []:
        return 0

    articles = {}

    for article in data['hits']['hits']: 
        try:
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
        except:
            continue

    return articles
 
def sent_analysis():

    query = {'size': 1000, 'query':{'match_all' : {}}}
    data = es.search(index='news-articles', body=query)
 
    if data['hits']['hits'] == []:
        return 0

    neutral = []    
    positive = []
    negative = []

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
    
    return {'positive': len(positive), 'negative': len(negative)} 


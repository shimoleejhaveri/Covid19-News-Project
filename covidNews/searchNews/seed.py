'''Feed Covid-19 news to Elasticsearch'''

import os
from elasticsearch import Elasticsearch
import requests
import json
import datetime
from pytz import timezone
from goose3 import Goose
import uuid

key = os.environ.get('API_KEY')
ip = os.environ.get('IP')

tz = timezone('US/Pacific')
date = str(datetime.datetime.now(tz))[:10]
time = str(datetime.datetime.now(tz))[11:19]

def callNewsApi(startdate, key):
    '''Call the News API'''

    keywords = ['covid-19', 'covid', 'coronavirus']

    url = (('http://newsapi.org/v2/everything?'
           'q=' + 
           ' OR '.join(keywords)) +
           '&from=' + date +
           '&language=en' +
           '&sortBy=popularity' +
           '&apiKey=' + key)

    response = requests.get(url)

    return response.json()

def extractText(url):
    '''Extract text from the URL'''

    extractor = Goose()
    extracted_article = extractor.extract(url=url)
    text = extracted_article.cleaned_text[:10000]

    return text

def addArticles(response, es):
    '''Add articles with unique IDs to Elasticsearch'''

    dic_article={}

    for article in response['articles']:
        try:
            if article['source']['name'] != 'null':
                dic_article['source_name'] = article['source']['name']

            if article['description'] != 'null':
                dic_article['description'] = article['description']

            if article['author'] != 'null':
                dic_article['author'] = article['author']

            if article['title'] != 'null':
                dic_article['title'] = article['title']

            if article['url'] != 'null':
                request = requests.get(article['url'])

                if request.status_code == 200:
                    dic_article['url'] = article['url']
                else:
                    continue

            if article['publishedAt'] != 'null':
                dic_article['publishedAt'] = str(article['publishedAt'][:10]).replace(' ', '')
                dic_article['timeAt'] = str(article['publishedAt'][11:19]).replace(' ', '')
                
            text = extractText(article['url'])
            dic_article['content'] = text
            
            new_id = uuid.uuid4()

            a = es.index(index='news-articles', id=new_id, body=dic_article)
            print('THIS WORKED', a)

        except:
            continue

def feedEs():
    '''Connect to Elasticsearch, create indices and populate the database'''

    es = Elasticsearch(['http://'+ip])

    if not es.indices.exists(index='news-articles'):
        es.indices.create(index='news-articles', ignore=400) 
  
    response = callNewsApi(date, key)
    addArticles(response, es)
    print('THIS WORKED TOO')
        
if __name__ == '__main__':
    feedEs()
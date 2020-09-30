'''Feed Covid-19 news to Elasticsearch'''

import os
from elasticsearch import Elasticsearch
import requests
import json
from datetime import datetime, date, timedelta
from backports.datetime_fromisoformat import MonkeyPatch
from pytz import timezone
from goose3 import Goose
from prediction import predict_sentiment
import hashlib
MonkeyPatch.patch_fromisoformat()

key = os.environ.get('API_KEY')
ip = os.environ.get('IP')

es = Elasticsearch(['http://' + ip])

def call_news_api(startdate, key):
    '''Call the News API'''

    keywords = ['covid-19', 'covid', 'coronavirus']

    url = (('http://newsapi.org/v2/everything?'
           'q=' + 
           ' OR '.join(keywords)) +
           '&from=' + startdate +
           '&language=en' +
           '&sortBy=popularity' +
           '&apiKey=' + key)

    response = requests.get(url)

    return response.json()

def extract_text(url):
    '''Extract text from the URL'''

    extractor = Goose()
    extracted_article = extractor.extract(url=url)
    text = extracted_article.cleaned_text[:10000]

    return text

def get_max_fetched_at(es):
    '''Get date of the last time articles were fetched from the ES database'''

    default_dt = (datetime.now() - timedelta(days=30)).isoformat()
    query = {'size': 1, 'sort' : [{'fetchedAt' : {'order' : 'desc', 'mode': 'max', 'unmapped_type' : 'keyword'}}]}
    data = es.search(index="news-articles", body=query)
    
    if data['hits']['hits']:
        data['hits']['hits'][0].get('fetchedAt', default_dt)
    
    return default_dt

def add_articles(response, es, fetched_at):
    '''Add articles with unique IDs to Elasticsearch'''

    dic_article={}

    # print("HELLO")

    for article in response['articles']:
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

        dic_article['createdAt'] = datetime.now().isoformat()
        # print("\n\n\n", "This is created_at", dic_article['createdAt'])
        
        dic_article['fetchedAt'] = fetched_at
        # print("\n\n\n", "This is fetched_at", dic_article['fetchedAt'])

        # print("HELLO")

        text = extract_text(article['url'])
        dic_article['content'] = text
        
        new_id = hashlib.md5(dic_article['url'].encode()).hexdigest() 
        # print("THIS IS NEW_ID", new_id)

        a = es.index(index="news-articles", id=new_id, body=dic_article)

def seed_daily():
    '''Connect to Elasticsearch, create indices and populate the database'''
    
    if not es.indices.exists(index="news-articles"):
        es.indices.create(index="news-articles", ignore=400) 
    
    max_fetched_at = get_max_fetched_at(es)
    print("\n\n\n","This is max_fetched_at", max_fetched_at)

    dt = datetime.fromisoformat(max_fetched_at)
    print("\n\n\n", "This is dt", dt)

    last_fetched_at = dt.date().isoformat()
    print("\n\n\n", "This is last_fetched_at", last_fetched_at)
    print("\n\n\n", "This is last_fetched_at type", type(last_fetched_at))

    new_fetched_at = datetime.utcnow()
    print("\n\n\n", "This is new_fetched_at", new_fetched_at)
    
    response = call_news_api(last_fetched_at, key)
    # print("\n\n\n", "This is response", response)

    add_articles(response, es, new_fetched_at)

    # query = {'size': 500, 'query': {'match': {'publishedAt': last_fetched_at}}}
    query = {'size': 500, 'query': {'match_all': {}}}
    # print(query)
    data = es.search(index="news-articles", body=query)
    print("\n\n\n\n", "THIS IS THE DATA", data)

    predict_sentiment(data, es)

seed_daily()

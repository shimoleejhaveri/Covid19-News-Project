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

def call_news_api(startdate, enddate, key):
    '''Call the News API'''

    keywords = ['covid-19', 'covid', 'coronavirus', 'pandemic']

    url = (('http://newsapi.org/v2/everything?'
           'q=' + 
           ' OR '.join(keywords)) +
           '&from=' + startdate +
           '&to=' + enddate +
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
        return data['hits']['hits'][0]['_source'].get('fetchedAt', default_dt)
    
    return default_dt

def add_articles(response, es, fetched_at):
    '''Add articles with unique IDs to Elasticsearch'''

    dic_article={}

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
        dic_article['fetchedAt'] = fetched_at
        
        # The content has been removed for simplicity raison
        # text = extract_text(article['url'])
        # dic_article['content'] = text
        
        new_id = hashlib.md5(dic_article['url'].encode()).hexdigest() 
        print(dic_article['publishedAt'])
    
        a = es.index(index="news-articles", id=new_id, body=dic_article)
        print('the result', a['result'])

def seed_daily():
    '''Create indices and populate the database'''
    
    if not es.indices.exists(index="news-articles"):
        es.indices.create(index="news-articles", ignore=400) 
    
    max_fetched_at = get_max_fetched_at(es)
    dt = datetime.fromisoformat(max_fetched_at)

    last_fetched_at = str(dt.date().isoformat())
    new_fetched_at = str(datetime.utcnow().date())

    # get the date of the last published article 
    query = {'size': 1, 'sort' : [{'publishedAt' : {'order' : 'desc', 'mode': 'max', 'unmapped_type' : 'keyword'}}]}
    data = es.search(index="news-articles", body=query)
    max_published_at = datetime.fromisoformat(data['hits']['hits'][0]['_source']['publishedAt'])
    last_published_at = str(max_published_at.date()) 

    if last_fetched_at > last_published_at: 
        last_published_at = datetime.fromisoformat(last_published_at) + timedelta(days=1)
        last_fetched_at = last_published_at

    # call news api
    response = call_news_api(last_fetched_at, new_fetched_at, key)

    # add the articles to the elasticsearch
    add_articles(response, es, new_fetched_at)

    # predict sentiments
    query = {'size': 10000, "query": {"range": {"publishedAt": {"from": last_fetched_at, "to": new_fetched_at}}}}      
    data = es.search(index="news-articles", body=query)
    print(len([d["_source"] for d in data['hits']['hits']]))  
    predict_sentiment(data, es)

    

if __name__ == '__main__':    
    seed_daily()



'''Feed Covid News'''

from elasticsearch import Elasticsearch
import requests
from dataclasses import dataclass
import json
from datetime import datetime, date, timedelta
from os import environ
from goose3 import Goose
from requests import get
import uuid
import dateutil.relativedelta

def get_time(date):
    # get the time from publishedAt': '2020-06-18T22:24:00Z

    return (date.split('T'))[1]

def get_date(date):
    # get the date from publishedAt': '2020-06-18T22:24:00Z
    return (date.split('T'))[0]

def callNewsApi(startdate, enddate, key):
    '''call the news api'''

    return (requests.get("http://newsapi.org/v2/everything?q=Covid&from="+startdate+"&to="+enddate+"&sortBy=publishedAt&pageSize=20&language=en&apiKey="+key)).json()

def extractText(url):
    '''extract text'''

    extractor = Goose()
    extracted_article = extractor.extract(url=url)
    text = extracted_article.cleaned_text[:10000]

    return text

def addarticles(response):
    '''add articles to the Elastcisearch'''

    dic_article={}
    for article in response["articles"]:
        try:
            if article["source"]["name"] != "null":
                dic_article["source_name"] = article["source"]["name"]

            if article["description"] != "null":
                dic_article["description"] = article["description"]

            if article["author"] != "null":
                dic_article["author"] = article["author"]

            if article["title"] != "null":
                dic_article["title"] = article["title"]

            if article["url"] != "null":
                print(article["url"])
                request = requests.get(article["url"])
                # check if the url is valid
                if request.status_code == 200:
                    dic_article["url"] = article["url"]
                else:
                    continue

            if article["publishedAt"] != "null":
                # publishedAt': '2020-06-18T22:24:00Z
                dic_article["publishedAt"] = get_date(article["publishedAt"])
                dic_article["timeAt"] = get_time(article["publishedAt"])

            # extract the article from its URL
            text = extractText(article["url"])
            dic_article["content"] = text

            # get the new id
            new_id = uuid.uuid4()

            # add to elasticsearch
            a = es.index(index="news-articles", id=new_id, body=dic_article)
            print('\n\n\n\n\n', "this is a", a)
        except:
            continue

def feedEs():
    '''connect to the Elasticsearch, create the index and feed the data to the elasticsearch'''

    key=environ.get('API_KEY')
    ip=environ.get('IP')

    # connect to elasticsearch
    es=Elasticsearch(["http://"+ip])

    # create an index
    if not es.indices.exists(index="news-articles"):
        es.indices.create(index='news-articles', ignore=400) 

    # get today's date and a date of a month ago 
    now = datetime.now()
    lastMonth = now + dateutil.relativedelta.relativedelta(months=-1)
    number_days = (now - lastMonth).days

    for i in range(1,number_days+1):
        search_date = str((lastMonth + timedelta(days=i)).date())  
        response = callNewsApi(search_date, search_date, key)
        addarticles(response)
        
    return

feedEs()

   
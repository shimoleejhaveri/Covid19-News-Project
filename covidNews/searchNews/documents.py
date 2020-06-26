'''Covid News'''

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

def feedEs():
    '''feed the data to the elasticsearch'''

    key=environ.get('API_KEY')
    ip=environ.get('IP')

    # connect to elasticsearch
    es=Elasticsearch(["http://"+ip])

    # create an index
    if not es.indices.exists(index="news-articles"):
        es.indices.create(index='news-articles', ignore=400) 

    # get today's date
    now = datetime.now()
    lastMonth = now + dateutil.relativedelta.relativedelta(months=-1)
    number_days = (now - lastMonth).days

    for i in range(1,number_days+1):
        search_date = str((lastMonth + timedelta(days=i)).date())  
        response = (requests.get("http://newsapi.org/v2/everything?q=Covid&from="+search_date+"&to="+search_date+"&sortBy=publishedAt&pageSize=20&language=en&apiKey="+key)).json()
        # http://newsapi.org/v2/everything?q=Covid&from=2020-05-25&to=2020-05-29&sortBy=publishedAt&pageSize=50&language=en&apiKey=ca13cbd006dd4c4eb90c3cafd026768e
        dic_articles={}
        extractor = Goose()

        for article in response["articles"]:
            try:
                if article["source"]["name"] != "null":
                    dic_articles["source_name"] = article["source"]["name"]

                if article["description"] != "null":
                    dic_articles["description"] = article["description"]

                if article["author"] != "null":
                    dic_articles["author"] = article["author"]

                if article["title"] != "null":
                    dic_articles["title"] = article["title"]

                if article["url"] != "null":
                    print(article["url"])
                    request = requests.get(article["url"])
                    # check if the url is valid
                    if request.status_code == 200:
                        dic_articles["url"] = article["url"]
                    else:
                        continue

                if article["publishedAt"] != "null":
                    # publishedAt': '2020-06-18T22:24:00Z
                    dic_articles["publishedAt"] = get_date(article["publishedAt"])
                    dic_articles["timeAt"] = get_time(article["publishedAt"])

                # extract the article from its URL
                extracted_article = extractor.extract(url=article["url"])
                text = extracted_article.cleaned_text[:10000]
                dic_articles["content"] = text

                # get the new id
                new_id = uuid.uuid4()

                # add to elasticsearch
                a = es.index(index="news-articles", id=new_id, body=dic_articles)
            except:
                continue

    return

   
'''Covid News'''

from elasticsearch import Elasticsearch
import requests
from dataclasses import dataclass
import json
from datetime import datetime, date, timedelta
import os
from goose3 import Goose
from requests import get
import uuid
import dateutil.relativedelta

key=os.environ.get('API_KEY')
ip=os.environ.get('IP')

def addarticle():
    
    search_topic="Covid_19"
    search_date="2020-08-03" ## write fn to get current date
    
    response = (requests.get("http://newsapi.org/v2/everything?q=Covid&from=2020-08-03&sortBy=publishedAt&language=en&apiKey="+key)).json()
    es=Elasticsearch(["http://"+ip])
    es.indices.create(index='news-articles', ignore=400)
    dic_articles={}
    extractor = Goose()

    for i, article in enumerate(response["articles"]):
        if article["source"]["name"] != "null":
            dic_articles["source_name"] = article["source"]["name"]

        if article["description"] != "null":
            dic_articles["description"] = article["description"]

        if article["author"] != "null":
            dic_articles["author"] = article["author"]

        if article["title"] != "null":
            dic_articles["title"] = article["title"]

        if article["url"] != "null":
            dic_articles["url"] = article["url"]

        if article["publishedAt"] != "null":
            dic_articles["publishedAt"] = article["publishedAt"]

        # extract the article from its URL
        extracted_article = extractor.extract(url=article["url"])
        text = extracted_article.cleaned_text[:10000]
        dic_articles["content"] = text

        # add to elasticsearch
        a = es.index(index="news-articles", id=i, body=dic_articles)
    #test if we saved in the created index a document that has the id 3 
    b = es.get(index="news-articles", id=3)['_source']
    # print(b)

    #return the content of the the checked document 
    return b["content"]


def displayNews():

    payload = {"q": "Covid", "from": "2020-08-03", "sortBy": "publishedAt", "language": "en", "apiKey": key}

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
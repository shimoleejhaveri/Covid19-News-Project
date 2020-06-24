'''Covid News'''

from elasticsearch import Elasticsearch
import requests
from dataclasses import dataclass
import json
from datetime import datetime
from os import environ
from goose3 import Goose
from requests import get

def addarticle():
    key=environ.get('API_KEY')
    ip=environ.get('IP')
    
    searchtopic="Covid_19"
    search_date="2020-06-11"
    
    response = (requests.get("http://newsapi.org/v2/everything?q=Covid&from=2020-06-11&sortBy=publishedAt&language=en&apiKey="+key)).json()
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
    print(b)

    #return the content of the the checked document 
    return b["content"]




    # extractor = Goose()
    # article = extractor.extract(url='https://cebudailynews.inquirer.net/318072/cebuano-visual-artist-produces-fashionable-turbans-to-raise-funds-for-covid-19-frontliners')
    # print(article.title)
    # text=article.cleaned_text[:10000]

    
    
    # es.indices.create(index='my-articles', ignore=400)
    # a = es.index(index="my-articles", id=1, body={"any": "data", "timestamp": datetime.now()})
    # b = es.get(index="my-articles", id=1)['_source']
    # print(b)
    


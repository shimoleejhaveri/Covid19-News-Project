'''Covid News'''

from elasticsearch import Elasticsearch
import requests
from dataclasses import dataclass
import json
from datetime import datetime
from os import environ

def addarticle():
    key=environ.get('API_KEY')
    ip=environ.get('IP')
    
    response = (requests.get("http://newsapi.org/v2/everything?q=Covid&from=2020-06-11&sortBy=publishedAt&language=en&apiKey="+key)).json()
    es=Elasticsearch(["http://"+ip])
    print(response["articles"][1]["content"])
    return response
    
    # es.indices.create(index='my-articles', ignore=400)
    # a = es.index(index="my-articles", id=1, body={"any": "data", "timestamp": datetime.now()})
    # b = es.get(index="my-articles", id=1)['_source']
    # print(b)
    
    # print(es.cluster.state())

    # The act of storing data in Elasticsearch is called indexing.
    # e1={
    #     "first_name":"nitin",
    #     "last_name":"panwar",
    #     "age": 27,
    #     "about": "Love to play cricket", 
    #     "interests": ['sports','music'],
    # }
    
    # es.indices.create(index='my-articles', ignore=400)
    # a = es.index(index="my-articles", id=42, body={"any": "data", "timestamp": datetime.now()})
    # b = es.get(index="my-articles", id=42)['_source']
    # print(a)
    # print("\n")
    # print(b)

    # index_test = requests.put('http://10.0.0.248:9200/test_index/test1/1',data=e1) # this line is successful
    # es.create(index="test", doc_type="articles", id=1, body={"content": "One more fox"})

    # res1 = es.search(index="test", doc_type="articles", body={"query": {"match": {"content": "fox"}}})
    # print(res1)
    # res = es.search(index="test_index", doc_type="atest1", body={"query": {"match": {"first_name": "nitin"}}})
    # print(res)
    # check_settings = requests.get('http://10.0.0.248:9200/test_index/test1')
    # print(check_settings.json())
'''Seed the data everyday '''

import os
from elasticsearch import Elasticsearch
from datetime import datetime, date
from prediction import predict_sentiment
from seed import addarticles, callNewsApi

# get the ip and the key
ip = os.environ.get('IP')
key = os.environ.get('API_KEY')

# connect to elasticsearch
es = Elasticsearch(["http://"+ip])


# get today's date 
now = datetime.now()

# Get the new using the news API 
date = str(now.date()) 
response = callNewsApi(date, date, key)

# Add the news to the index
addarticles(response, es) 

# predict sentiments 
query = {"size": 1000,"query":{"match":{"publishedAt": '2020-09-09'}}}
data = es.search(index="news-articles", body=query)
print(data)

for a in data['hits']['hits']: 
    print(a['_source']['description'],'\n')


# predict sentiment and add to the Elasticsearch database
predict_sentiment(data, es)

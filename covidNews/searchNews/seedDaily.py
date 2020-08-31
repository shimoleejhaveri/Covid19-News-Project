'''Seed the data everyday '''

import os
from elasticsearch import Elasticsearch
import datetime
from pytz import timezone
from prediction import predict_sentiment
from seed import addarticles, callNewsApi


def seedDaily():
	# get the ip and the key
	ip = os.environ.get('IP')
	key = os.environ.get('API_KEY')

	# connect to elasticsearch
	es = Elasticsearch(["http://"+ip])

	tz = timezone("US/Pacific")
	
	today = str(datetime.datetime.now(tz))[:10]
	
	response = callNewsApi(today, key)

	# Add the news to the index
	addarticles(response, es)

	# predict sentiments 
	query = {"size": 500,"query":{"match":{"publishedAt": today}}}
	data = es.search(index="news-articles", body=query)

	# predict sentiment and add to the Elasticsearch database
	predict_sentiment(data, es)

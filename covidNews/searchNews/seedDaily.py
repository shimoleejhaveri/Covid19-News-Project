'''Seed the data everyday '''

import os
from elasticsearch import Elasticsearch
import datetime
from pytz import timezone
from prediction import predict_sentiment
from seed import addArticles, callNewsApi

ip = os.environ.get('IP')
key = os.environ.get('API_KEY')

es = Elasticsearch(["http://"+ip])

tz = timezone("US/Pacific")
today = str(datetime.datetime.now(tz))[:10]

def seedDaily():
	'''Seed Elasticsearch database daily with news articles and perform sentiment analysis on them'''

	response = callNewsApi(today, key)
	addArticles(response, es)

	# predict sentiments 
	query = {"size": 500,"query":{"match":{"publishedAt": today}}}
	data = es.search(index="news-articles", body=query)

	# predict sentiment and add to the Elasticsearch database
	predict_sentiment(data, es)

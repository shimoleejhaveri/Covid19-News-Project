'''Populate initial database with a month's worth of news articles'''

import os
import requests
import json
import datetime
from elasticsearch import Elasticsearch
from seed import add_articles
from prediction import predict_sentiment

def populate_database():
	
	key = os.environ.get('API_KEY')
	ip = os.environ.get('IP')

	es = Elasticsearch(['http://'+ip])

	today = datetime.datetime.now()
	now = str(today)[:10]
	# yesterday = str(today - datetime.timedelta(days=1))[:10]
	last_month = str(today - datetime.timedelta(days=30))[:10]

	keywords = ['covid-19', 'covid', 'coronavirus']

	url = (('http://newsapi.org/v2/everything?'
           'q=' + 
           ' OR '.join(keywords)) +
           '&from=' + last_month +
           '&to=' + now +
           '&language=en' +
           '&sortBy=popularity' +
           '&apiKey=' + key)

	info = requests.get(url)
	response = info.json()

	add_articles(response, es, now)

	query = {'size': 10000, 'query': {'match_all' : {}}}
	data = es.search(index='news-articles', body=query)

	predict_sentiment(data, es)

if __name__ == '__main__':
	populate_database()
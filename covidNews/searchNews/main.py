'''Populate initial database with a month's worth of news articles'''

import os
import requests
import json
import datetime
from elasticsearch import Elasticsearch
from pytz import timezone
from seed import addArticles
from predict import predictSentiment

def populateDatabase():
	
	key=os.environ.get('API_KEY')
	ip=os.environ.get('IP')

	es = Elasticsearch(['http://'+ip])

	tz = timezone('US/Pacific')
	today = datetime.datetime.now(tz)
	yesterday = str(today - datetime.timedelta(days=1))[:10]
	last_month = str(today - datetime.timedelta(days=30))[:10]

	keywords = ['covid-19', 'covid', 'coronavirus']

	url = (('http://newsapi.org/v2/everything?'
           'q=' + 
           ' OR '.join(keywords)) +
           '&from=' + last_month +
           '&to=' + yesterday +
           '&language=en' +
           '&sortBy=popularity' +
           '&apiKey=' + key)

	info = requests.get(url)
	response = info.json()

	addArticles(response, es)

	query = {'size': 500000, 'query':{'match_all' : {}}}
    data = es.search(index='news-articles', body=query)

    predictSentiment(data, es)

if __name__ == '__main__':
	populateDatabase()
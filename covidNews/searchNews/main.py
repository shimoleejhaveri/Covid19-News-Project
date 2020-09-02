'''Populate initial database with a month's worth of news articles'''

import os
from elasticsearch import Elasticsearch
import requests
import json
from pytz import timezone
import datetime
from seed import addArticles
from documents import sentAnalysis

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
	print(response['totalResults'])
	addArticles(response, es)

	query = {'size': 500000, 'query':{'match_all' : {}}} # which publishedAt date to add here to query? \
	# should we not not add the date altogether, and just run sentiment analysis on the whole dataset?
    data = es.search(index='news-articles', body=query)

    predictSentiment(data, es)

	# check with Imen whether to call predictSentiment() or sentAnalysis()
# populateDatabase()
if __name__ == '__main__':
	populateDatabase()
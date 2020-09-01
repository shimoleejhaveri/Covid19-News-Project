'''Cron job to call News API at 11 pm PST and seed the database daily'''

import os
from elasticsearch import Elasticsearch
import requests
from pytz import timezone
import datetime
from seed import addArticles, callNewsApi
from seedDaily import seedDaily

key=os.environ.get('API_KEY')
ip=os.environ.get('IP')

es=Elasticsearch(['http://'+ip])

tz = timezone('US/Pacific')
today = str(datetime.datetime.now(tz))[:10]

def callApi():
	
	print('cron =', es.indices.exists(index='news-articles'))

	response = callNewsApi(today, key)
	addArticles(response, es)
	seedDaily()

	print('END')

callApi()
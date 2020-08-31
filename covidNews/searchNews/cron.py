import os
from elasticsearch import Elasticsearch
import requests
from pytz import timezone
import datetime
from seed import addarticles, callNewsApi
from seedDaily import seedDaily

def callApi():
	key=os.environ.get('API_KEY')
	ip=os.environ.get('IP')

	es=Elasticsearch(["http://"+ip])
	print("cron =", es.indices.exists(index="news-articles"))

	tz = timezone("US/Pacific")
	today = str(datetime.datetime.now(tz))[:10]
	
	response = callNewsApi(today, key)
	addarticles(response, es)
	seedDaily()

	print("END")
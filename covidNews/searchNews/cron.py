'''Cron job to call News API at 11 pm PST and seed the database daily'''

import os
from elasticsearch import Elasticsearch
import requests
from pytz import timezone
import datetime
from seed import seed_daily

def call_api():
	
	ip = os.environ.get('IP')
	es = Elasticsearch(['http://'+ip])
	
	print('cron =', es.indices.exists(index='news-articles')) # sanity check to see if ES is working

	seed_daily()

call_api()
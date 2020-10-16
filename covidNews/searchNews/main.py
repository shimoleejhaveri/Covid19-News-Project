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
  lmonth = today - datetime.timedelta(days=30)

  keywords = ['covid-19', 'covid', 'coronavirus', 'pandemic']

  for single_date in (lmonth + datetime.timedelta(days=n) for n in range(31)):
    try:
      todays_date = str(single_date)[:10]
      print('single_date', single_date, todays_date)
      url = (('http://newsapi.org/v2/everything?'
             'q=' + 
             ' OR '.join(keywords)) +
             '&from=' + todays_date +
             '&to=' + todays_date +
             '&language=en' +
             '&sortBy=popularity' +
             '&apiKey=' + key)

      info = requests.get(url)
      response = info.json()

      add_articles(response, es, now)

      query = {'size': 10000, "query": {"range": {"publishedAt": {"from": todays_date, "to": todays_date}}}}
      data = es.search(index='news-articles', body=query)

      predict_sentiment(data, es)
    except:
      continue

if __name__ == '__main__':
	populate_database()
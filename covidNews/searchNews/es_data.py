import csv
import os
from elasticsearch import Elasticsearch

ip = os.environ.get('IP')
es = Elasticsearch(['http://'+ip])

query = {'size': 1000, 'query':{'match_all' : {}}}
data = es.search(index='news-sentiment', body=query)

with open('final.csv', 'a+', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter='|',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)

    filewriter.writerow(['publishedAt', 'description', 'sentiment'])  

    for article in data['hits']['hits']:
        sentiment = article['_source']['sentiment']
        description = article['_source']['description']
        publishedAt = article['_source']['publishedAt']

        filewriter.writerow([str(publishedAt), description, str(sentiment)])
            
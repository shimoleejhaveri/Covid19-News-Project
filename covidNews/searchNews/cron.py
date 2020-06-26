from elasticsearch import Elasticsearch
import requests
from dataclasses import dataclass
import json
from datetime import datetime, date
from os import environ
from goose3 import Goose
from requests import get
import uuid
from searchNews.seed import addarticles, callNewsApi

# from seed import *

def callapi():
    # key=environ.get('API_KEY')
    # ip=environ.get('IP')

    ip='10.0.0.248:9200'
    key='ca13cbd006dd4c4eb90c3cafd026768e'

    # connect to elasticsearch
    es=Elasticsearch(["http://"+ip])
    print("cron", es.indices.exists(index="news-articles"))

    startdate = str((datetime.now()).date())
    response = seed.callNewsApi(startdate, startdate, key)
    seed.addarticles(response)
    






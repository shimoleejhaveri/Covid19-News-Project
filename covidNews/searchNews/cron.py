import os
from elasticsearch import Elasticsearch
import requests
from dataclasses import dataclass
import json
from datetime import datetime, date
from requests import get
import uuid
from searchNews.seed import addarticles, callNewsApi

# from seed import *

def callapi():
    key=os.environ.get('API_KEY')
    ip=os.environ.get('IP')

    # connect to elasticsearch
    es=Elasticsearch(["http://"+ip])
    print("cron", es.indices.exists(index="news-articles"))

    startdate = str((datetime.now()).date())
    response = seed.callNewsApi(startdate, startdate, key)
    seed.addarticles(response,es)
    






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

<<<<<<< Updated upstream
# from seed import *

def callapi():
    key=environ.get('API_KEY')
    ip=environ.get('IP')
=======
def callApi():
    key=os.environ.get('API_KEY')
    ip=os.environ.get('IP')
>>>>>>> Stashed changes

    # connect to elasticsearch
    es=Elasticsearch(["http://"+ip])
    print("cron", es.indices.exists(index="news-articles"))

    startdate = str((datetime.now()).date())
<<<<<<< Updated upstream
    response = seed.callNewsApi(startdate, startdate, key)
    seed.addarticles(response)
    





=======
    response = callNewsApi(startdate, startdate, key)
    addarticles(response, es)
    
>>>>>>> Stashed changes

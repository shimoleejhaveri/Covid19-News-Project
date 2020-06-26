'''Covid News'''

from elasticsearch import Elasticsearch
import requests
from dataclasses import dataclass
import json
from datetime import datetime, date, timedelta
from os import environ
from goose3 import Goose
from requests import get
import uuid
import dateutil.relativedelta

def sentAnalysis():
    return "the code goes here"
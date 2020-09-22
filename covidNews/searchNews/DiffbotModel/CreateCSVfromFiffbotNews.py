import csv
import pandas as pd
import numpy as np
import os
from elasticsearch import Elasticsearch


# connect to elasticsearch
# ip = os.environ.get('IP')
# es = Elasticsearch(["http://"+ip])


data = pd.read_csv("diffbotNews.csv", delimiter='|', names = ['id','published_at', 'sentiment', 'description']) 
df = pd.DataFrame(data)

# Remove missing values (NaN)
df = df[pd.notnull(df['description'])]
s = set()

with open('diffbotFinal222.csv', 'a+', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter='|',
                         quoting=csv.QUOTE_MINIMAL)

    for i,r in df.iterrows():
        # query = {"size": 1,"query":{"match":{"_id": r['id']}}}
        # data = es.search(index="news-articles", body=query)
        # for article in data['hits']['hits']:
        #     try:
        #         content = article['_source']['content']
        #     except:
        #         continue

        if r['description'] not in s:
            s.add(r['description'])
        if float(r['sentiment']) < 0:
            filewriter.writerow([r['published_at'], r['description'], '1'])
        if float(r['sentiment']) > 0:
            filewriter.writerow([r['published_at'], r['description'], '2'])
        if float(r['sentiment']) == 0:
            filewriter.writerow([r['published_at'], r['description'], '0'])
print(len(s))




# import csv
# import pandas as pd
# import numpy as np

# data = pd.read_csv("diffbotNews.csv", delimiter='|', names = ['id','published_at', 'sentiment', 'description']) 
# df = pd.DataFrame(data)

# # Remove missing values (NaN)
# df = df[pd.notnull(df['description'])]
# s = set()

# with open('diffbotFinal.csv', 'a+', newline='') as csvfile:
#     filewriter = csv.writer(csvfile, delimiter='|',
#                         quotechar='|', quoting=csv.QUOTE_MINIMAL)

#     for i,r in df.iterrows():
#         if r['description'] not in s:
#             s.add(r['description'])
#             if float(r['sentiment']) < 0:
#                 filewriter.writerow([r['published_at'], r['description'], '1'])
#             if float(r['sentiment']) > 0:
#                 filewriter.writerow([r['published_at'], r['description'], '2'])
#             if float(r['sentiment']) == 0:
#                 filewriter.writerow([r['published_at'], r['description'], '0'])
# print(len(s))
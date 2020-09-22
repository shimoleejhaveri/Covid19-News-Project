import requests
import os
from elasticsearch import Elasticsearch
import csv


# connect to elasticsearch
ip = os.environ.get('IP')
es = Elasticsearch(["http://"+ip])

query = {"size": 1000,"query":{"match_all" : {}}}
data = es.search(index="news-articles", body=query)

articles = {}

with open('diffbotNews.csv', 'a+', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter='|',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # filewriter.writerow(['id', 'published_at', 'text', 'sentiment'])  

    for article in data['hits']['hits']: 
        try:
            date = article['_source']['publishedAt']
            description = article['_source']['description']
            content = article['_source']['content']
            url_news = article['_source']['url']

            # Call the API
            artcile_api = 'http://api.diffbot.com/v3/article?token=b605b9867797931a754cb95621b46551&url='
            # url = 'https://www.justgivemepositivenews.com/'

            request = requests.get(artcile_api+url_news).json()
            # request = {"request":{"pageUrl":"https://www.justgivemepositivenews.com/","api":"article","version":3},"objects":[{"date":"Tue, 08 Sep 2020 00:00:00 GMT","sentiment":0.652,"images":[{"naturalHeight":492,"width":740,"diffbotUri":"image|3|1853375060","url":"https://www.justgivemepositivenews.com/uploads/1/3/1/3/131348198/screenshot-2020-09-08-at-12-10-14_orig.png","naturalWidth":759,"primary":True,"height":479},{"naturalHeight":489,"width":725,"diffbotUri":"image|3|56423701","url":"https://www.justgivemepositivenews.com/uploads/1/3/1/3/131348198/screenshot-2020-09-08-at-12-10-24_orig.png","naturalWidth":725,"height":489}],"estimatedDate":"Tue, 08 Sep 2020 20:41:41 GMT","diffbotUri":"article|3|910318474","siteName":"Just Give Me Positive Good News","type":"article","title":"JUST POSITIVE GOOD NEWS ABOUT COVID-19","tags":[{"score":0.9953998923301697,"sentiment":-0.894,"count":3,"label":"COVID-19","uri":"https://diffbot.com/entity/XkFmXKkFZMNWNCjQC5MfwUw","rdfTypes":["http://dbpedia.org/ontology/Disease"]},{"score":0.9063773155212402,"sentiment":0,"count":1,"label":"Office for National Statistics","uri":"https://diffbot.com/entity/C0b02zCvhNBKjtDyoOrV5IQ","rdfTypes":["http://dbpedia.org/ontology/Organisation","http://dbpedia.org/ontology/Place"]}],"humanLanguage":"en","pageUrl":"https://www.justgivemepositivenews.com/","html":"<p>Weekly coronavirus deaths have dropped to the lowest number in England and Wales since mid-March, new statistics suggest.<\/p>\n<p>Data from the Office for National Statistics shows a total of 101 deaths registered in the week ending August 28 mentioned Covid-19 on the death certificate.<\/p>\n<p>This is down from 138 deaths in the previous week.<\/p>\n<p>It is also the lowest number since the week ending March 13, when five deaths involving Covid-19 were registered.<\/p>\n<p><a href=\"https://www.standard.co.uk/news/uk/england-wales-weekly-coronavirus-deaths-drop-a4542371.html\">https://www.standard.co.uk/news/uk/england-wales-weekly-coronavirus-deaths-drop-a4542371.html<br>\n<br>\n<\/a><strong>HELP US SPREAD GOOD NEWS!<\/strong><\/p>\n<p>I run this site in my spare time and thoroughly enjoy giving you all positive news! If you've enjoyed the site we'd love for you to help me share the good news far and wide, share us on <a href=\"https://www.reddit.com/\">Reddit<\/a>, your <a href=\"https://www.facebook.com/\">Facebook<\/a> or your <a href=\"https://twitter.com/\">Twitter<\/a> and spread a little positivity around.<\/p>\n<p><strong>ENJOY FEEL GOOD, INSPIRING STORIES AND VIDEOS ?<\/strong><\/p>\n<p>Our <a href=\"https://www.justgivemepositivenews.com/goodnews.html\">new page here<\/a> is just what you need, with just good news, feel good stories unrelated to COVID.<\/p>\n<figure><a><img alt=\"Picture\" src=\"https://www.justgivemepositivenews.com/uploads/1/3/1/3/131348198/screenshot-2020-09-08-at-12-10-14_orig.png\"><\/img><\/a><\/figure>\n<figure><a><img alt=\"Picture\" src=\"https://www.justgivemepositivenews.com/uploads/1/3/1/3/131348198/screenshot-2020-09-08-at-12-10-24_orig.png\"><\/img><\/a><\/figure>","text":"Weekly coronavirus deaths have dropped to the lowest number in England and Wales since mid-March, new statistics suggest.\nData from the Office for National Statistics shows a total of 101 deaths registered in the week ending August 28 mentioned Covid-19 on the death certificate.\nThis is down from 138 deaths in the previous week.\nIt is also the lowest number since the week ending March 13, when five deaths involving Covid-19 were registered.\nhttps://www.standard.co.uk/news/uk/england-wales-weekly-coronavirus-deaths-drop-a4542371.html\nHELP US SPREAD GOOD NEWS!\nI run this site in my spare time and thoroughly enjoy giving you all positive news! If you've enjoyed the site we'd love for you to help me share the good news far and wide, share us on Reddit, your Facebook or your Twitter and spread a little positivity around.\nENJOY FEEL GOOD, INSPIRING STORIES AND VIDEOS ?\nOur new page here is just what you need, with just good news, feel good stories unrelated to COVID."}]}
            # print(request['objects'][0]['date'], '\n', request['objects'][0]['sentiment'],'\n', request['objects'][0]['title'],'\n\n\n\n\n\n', request['objects'][0]['text'])
            
            print(request['objects'][0]['date'])
            filewriter.writerow([article['_id'], date, request['objects'][0]['sentiment'], description])
        except:
            continue
               
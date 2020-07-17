from elasticsearch import Elasticsearch
import requests
import json
from os import environ
import nltk
import string
# from nltk import word_tokenize
# from nltk.corpus import stopwords
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.tokenize import sent_tokenize
from nltk.tokenize import TreebankWordTokenizer 
from nltk.tokenize import RegexpTokenizer 
from nltk.stem.porter import PorterStemmer
# import inflect
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer 
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.linear_model import SGDClassifier
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
# import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import numpy as np 

import csv
global str


def vaderSent_classification(text):
    '''get the score'''

    analyser = SentimentIntensityAnalyzer()
    vs = analyser.polarity_scores(text)

    return vs


def textblob_classification(text):

    blob = TextBlob(text)

    return blob.sentiment



def clean_text(text):
    # nltk.download('all')
    # lowercase
    text = text.lower()

    # convert numbers into words
    p = inflect.engine()
    words = text.split()
    checked_words = [word if not word.isdigit() else p.number_to_words(word) for word in words]
    text = ' '.join(checked_words)

    # remove ’ fron the text
    text_p = ''.join([char if char != '’' else '\'' for char in text])

    # remove punctuation
    text_p = "".join([char for char in text_p if char not in string.punctuation])

    return text_p


def pre_process(text):
    ''' Pre process and convert texts to a list of words'''

    text_p = clean_text(text)
    # text_p = text.translate(str.maketrans('', '', string.punctuation))
    # sentiment_analyser_word2verc(text_p)
    # Tokenization
    # sentense tokenize
    # sentences = sent_tokenize(text_p)
    # words = word_tokenize(text_p)

    # tokenizer = TreebankWordTokenizer() 
    tokenizer = RegexpTokenizer("[\w']+") # [] a set of characters you wish to match any alph or numeric char followed with ' and matches one or more occurrences of the pattern left to it.
    words = tokenizer.tokenize(text_p) 

    # Stopword Filtering
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    
    # Stemming
    # porter = PorterStemmer()
    # stemmed = [porter.stem(word) for word in checked_words]

    # lemmatization
    lemmatizer = WordNetLemmatizer() 
    lemmas = [lemmatizer.lemmatize(word, pos ='v') for word in filtered_words] 
    # past ense to present tense 
    # print(lemmas)

    # # Pos
    pos = pos_tag(lemmas)
    # print(pos)

    return lemmas


def check_sentiment(sentiment):
    # decide sentiment as positive, negative and neutral 
    if sentiment['compound'] >= 0.05 : 
        return 'positive'
  
    elif sentiment['compound'] <= - 0.05 : 
        return 'negative' 
  
    else : 
        return 'neutral' 

def check_polarity(sentiment):
    if sentiment.polarity > 0:
        return 'positive'
    elif sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def check_pandas():
    data = pd.read_csv("news.csv", delimiter='|', names = ['Description', 'Content', 'PublishedAt', 'vader_polarity', 'Sentiment_vader', 'blob_polarity', 'Sentiment_blob']) 
    # print(data.head())
    
    # print (data[['Content', 'Sentiment_blob']])

    df = pd.DataFrame(data)
    for ind in df.index: 
        print(df['Sentiment_vader'][ind]) 

def classify():
    key=environ.get('API_KEY')
    ip=environ.get('IP')



    # connect to elasticsearch
    es=Elasticsearch(["http://"+ip])
    # body = {"size": 500,"query":{"match":{"publishedAt": "2020-06-24"}}}

    query = {"size": 500, "query": {"match_all": {}}}
    b = es.search(index="news-articles", body=query)
    with open('news.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Description', 'Content', 'PublishedAt', 'vader_polarity', 'Sentiment_vader', 'blob_polarity', 'Sentiment_blob'])

        for source in b["hits"]["hits"]:
            date = source["_source"]["publishedAt"]
            description = ""
            if source["_source"]["description"]:
                description = clean_text(source["_source"]["description"])
            text = clean_text(source["_source"]["content"])

            vader_polarity = vaderSent_classification(text)['compound']
            sentiment_vader = check_sentiment(vaderSent_classification(text))

            blob_polarity = textblob_classification(text).polarity
            sentiment_blob = check_polarity(textblob_classification(text))
            filewriter.writerow([description, text, date, vader_polarity, sentiment_vader, blob_polarity, sentiment_blob])
            

    check_pandas()    
    
    # pre process
    # words = pre_process(text)
    # bag_of_words(words)
    # text_processed = createclusters(text)
    # labeing_data(text)
    # nltk_labeling(text)

    return


def split_data(data):
    total = len(data)
    training_ratio = 0.75
    training_data = []
    evaluation_data = []

    for indice in range(0, total):
        if indice < total * training_ratio:
            training_data.append(data[indice])
        else:
            evaluation_data.append(data[indice])

    return training_data, evaluation_data

def main():
    data = pd.read_csv("news.csv", delimiter='|', names = ['Description', 'Content', 'PublishedAt', 'vader_polarity', 'Sentiment_vader', 'blob_polarity', 'Sentiment_blob']) 
    df = pd.DataFrame(data)

    df.loc[df['Sentiment_vader']=='negative','Sentiment_vader'] = -1
    df.loc[df['Sentiment_vader']=='positive','Sentiment_vader'] = 1
    df.loc[df['Sentiment_vader']=='neutral','Sentiment_vader'] = 0

    df_x = df["Content"]
    df_y = df["Sentiment_vader"]
    print(df.head())

    x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.25,random_state=4)
    text = x_train.values.astype('U')

    #cv = CountVectorizer()
    cv = TfidfVectorizer(stop_words='english')
    x_traincv = cv.fit(text)
    vocab = x_traincv.vocabulary_
    print(vocab)
    print(x_traincv.idf_)
    vector = x_traincv.transform(text)  

    print(vector.shape)
    print(vector.toarray())
    # print(type(x_traincv))
    # x_traincv = cv.fit_transform(['covid is bad', 'covid is less'])
    # print(x_traincv.toarray())

    #vectorizer = TfidfVectorizer(stop_words='english')
    #X = vectorizer.fit_transform(x_train.values.astype('U'))
    # print(vectorizer.get_feature_names())
    # print(X.shape)

    #df_tfidf = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())
    #df_tfidf.reset_index().drop_duplicates(subset='index', keep='first').set_index('index')
    # print(df_tfidf)
    
    #tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    #tfidf_transformer.fit_transform(X)
    #df_idf = pd.DataFrame(tfidf_transformer.idf_, columns=["idf_weights"])
    # print(df_idf)
    # print(df_idf.sort_values(by=['idf_weights']))
    

    # X_test = cv.transform(test_data)

    # list_data = []
    # for ind in df.index: 
    #     list_data.append([df['Content'][ind], df['Sentiment_vader'][ind]])



    # train_data, test_data = split_data(list_data)
    # print(create_vectorizer(train_data, test_data))


main()




    # article talk about the us ==>0,1 UK
    # the content needs to be not empty ==>10
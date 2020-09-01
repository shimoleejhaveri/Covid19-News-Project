'''Test dataset cleanup and preprocess'''

from elasticsearch import Elasticsearch
import nltk
import string
from nltk.corpus import stopwords 
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer 
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import pandas as pd
from sklearn.model_selection import train_test_split
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import csv

def vaderSentClassification(text):
    '''get the score'''

    analyser = SentimentIntensityAnalyzer()
    vs = analyser.polarity_scores(text)
    return vs

def textblobClassification(text):

    blob = TextBlob(text)
    return blob.sentiment

def cleanText(text):
    
    text = text.lower()

    # convert numbers into words
    p = inflect.engine()
    words = text.split()
    checked_words = [word if not word.isdigit() else p.number_to_words(word) for word in words]
    text = ' '.join(checked_words)

    # remove ’ fron the text
    text_p = ''.join([char if char != '’' else '\'' for char in text])

    # remove punctuation
    text_p = ''.join([char for char in text_p if char not in string.punctuation])

    return text_p

def preprocess(text):
    ''' Pre process and convert texts to a list of words'''

    text_p = cleanText(text)
    
    words = tokenizer.tokenize(text_p) 

    # Stopword Filtering
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
 
    lemmatizer = WordNetLemmatizer() 
    lemmas = [lemmatizer.lemmatize(word, pos ='v') for word in filtered_words] 

    pos = pos_tag(lemmas)
    # print(pos)

    return lemmas

def checkSentiment(sentiment):
    # decide sentiment as positive, negative and neutral 
    if sentiment['compound'] >= 0.05 : 
        return 'positive'
  
    elif sentiment['compound'] <= - 0.05 : 
        return 'negative' 
  
    else : 
        return 'neutral' 

def checkPolarity(sentiment):
    if sentiment.polarity > 0:
        return 'positive'
    elif sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def checkPandas():
    data = pd.read_csv('news.csv', delimiter='|', names = ['Description', 'Content', 'PublishedAt', 'vader_polarity', 'Sentiment_vader', 'blob_polarity', 'Sentiment_blob']) 

    df = pd.DataFrame(data)
    for ind in df.index: 
        print(df['Sentiment_vader'][ind]) 

def classify():
    key=environ.get('API_KEY')
    ip=environ.get('IP')

    # connect to elasticsearch
    es=Elasticsearch(['http://'+ip])
    # body = {'size': 500,'query':{'match':{'publishedAt': '2020-06-24'}}}

    query = {'size': 500, 'query': {'match_all': {}}}
    b = es.search(index='news-articles', body=query)
    with open('news.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Description', 'Content', 'PublishedAt', 'vader_polarity', 'Sentiment_vader', 'blob_polarity', 'Sentiment_blob'])

        for source in b['hits']['hits']:
            date = source['_source']['publishedAt']
            description = ''
            if source['_source']['description']:
                description = cleanText(source['_source']['description'])
            text = cleanText(source['_source']['content'])

            vader_polarity = vaderSentClassification(text)['compound']
            sentiment_vader = checkSentiment(vaderSentClassification(text))

            blob_polarity = textblobClassification(text).polarity
            sentiment_blob = checkPolarity(textblobClassification(text))
            filewriter.writerow([description, text, date, vader_polarity, sentiment_vader, blob_polarity, sentiment_blob])
            

    checkPandas()    
    return

def splitData(data):
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
    data = pd.read_csv('news.csv', delimiter='|', names = ['Description', 'Content', 'PublishedAt', 'vader_polarity', 'Sentiment_vader', 'blob_polarity', 'Sentiment_blob']) 
    df = pd.DataFrame(data)

    df.loc[df['Sentiment_vader']=='negative','Sentiment_vader'] = -1
    df.loc[df['Sentiment_vader']=='positive','Sentiment_vader'] = 1
    df.loc[df['Sentiment_vader']=='neutral','Sentiment_vader'] = 0

    df_x = df['Content']
    df_y = df['Sentiment_vader']
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

main()
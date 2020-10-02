'''Analyse the Tweets and create CSV file with the tweets and the sentiments'''

import os
from tweepy import Stream, API, Cursor
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import pandas as pd
import csv
import re 
from textblob import TextBlob
import string
import preprocessor as p
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#HappyEmoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])

# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])

#Emoji patterns
emoji_pattern = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)

#combine sad and happy emoticons
emoticons = emoticons_happy.union(emoticons_sad)

def clean_tweets(tweet):
    stop_words = set(stopwords.words('english'))
    # print('\n\n\n\n\n', tweet._json['text'])
    
    
    #after tweepy preprocessing the colon symbol left remain after      
    #removing mentions
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    tweet = re.sub(r'"', '', tweet)
    tweet = re.sub(r'’', '', tweet)
    tweet = re.sub(r'RT YEESSSIIIRRR', '', tweet)
    tweet = re.sub(r'^RT\s', '', tweet)
    #replace consecutive non-ASCII characters with a space
    tweet = re.sub(r"https(\S+)(\w+)", '', tweet)
    #remove urls
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)
    #remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)
    #filter using NLTK library append it to a string
    filtered_tweet = []
    #looping through conditions
    word_tokens = word_tokenize(tweet)
    for w in word_tokens:
        #check tokens against stop words , emoticons and punctuations
        if w not in stop_words and w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(w)
    return ' '.join(filtered_tweet)
    #print(word_tokens)
    #print(filtered_sentence)return tweet
        

def add_tweet(tweet_id, date, tweet, sentiment):
    sentiment = sentiment_analysis(filtered_tweet)
    
def sentiment_analysis(sentiment):
    if float(sentiment) > 0:
        return 'positive'
    elif float(sentiment) == 0:
        return 'neutral'
    else:
        return 'negative'

consumer_key = os.environ.get('TWITTER_API_KEY')
consumer_secret = os.environ.get('TWITTER_SECRET_KEY')
access_token = os.environ.get('ACCESS_TOKEN')
access_secret = os.environ.get('ACCESS_SECRET')

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = API(auth)
print(api)

data = pd.read_csv("corona_tweets_05.csv", header =[1, 2])

with open('tweet.csv', 'a+', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter='|',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # filewriter.writerow(['id', 'published_at', 'text', 'sentiment'])  

    for i in range(0,1000):
        try:
            tweet_id = data.iloc[i, 0]
            tweet_sentiment = data.iloc[i, 1]
            tweet_json = api.get_status(tweet_id) 
            date = (tweet_json.created_at).date()
            sentiment = sentiment_analysis(tweet_sentiment)
            tweet_text = clean_tweets(tweet_json.text)
            # print(tweet_id, date, tweet_text, sentiment)

            filewriter.writerow([tweet_id, str(date), tweet_text, sentiment])
        except:
            continue

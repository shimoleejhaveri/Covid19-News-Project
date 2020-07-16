import os

from tweepy import Stream, API, Cursor
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# import emoji
import pandas as pd
import csv
import re #regular expression
from textblob import TextBlob
import string
import preprocessor as p


consumer_key = os.environ.get('TWITTER_API_KEY')
consumer_secret = os.environ.get('TWITTER_SECRET_KEY')
access_token = os.environ.get('ACCESS_TOKEN')
access_secret = os.environ.get('ACCESS_SECRET')

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = API(auth)
print(api)


# search_words=["covid19","covid-19","coronavirus"] 
search_words = ['covid19', 'covid-19', 'coronavirus']
#  date_since = "2020-05-21"  
date_since='2020-05-21'
tweets = Cursor(api.search, 'covid-19', lang="en", since=date_since, include_rts=False).items(10)
print('\n\n\n\n\n', tweets)

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
	
	word_tokens = word_tokenize(tweet)
	#after tweepy preprocessing the colon symbol left remain after      #removing mentions
	tweet = re.sub(r':', '', tweet)
	tweet = re.sub(r'‚Ä¶', '', tweet)
	#replace consecutive non-ASCII characters with a space
	tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)
	#remove emojis from tweet
	tweet = emoji_pattern.sub(r'', tweet)
	#filter using NLTK library append it to a string
	filtered_tweet = []
	#looping through conditions
	for w in word_tokens:
		#check tokens against stop words , emoticons and punctuations
		if w not in stop_words and w not in emoticons and w not in string.punctuation:
			filtered_tweet.append(w)
	return ' '.join(filtered_tweet)
	#print(word_tokens)
	#print(filtered_sentence)return tweet

def sentiment_analysis(filtered_tweet):
	blob = TextBlob(filtered_tweet)
	sentiment = blob.sentiment
	polarity = sentiment.polarity
	subjectivity = sentiment.subjectivity

	if sentiment.polarity > 0:
            return 'positive'
        elif sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

def add_tweet(filtered_tweet, sentiment):
	created_at = clean_tweets(tweet._json['created_at'])
	source = clean_tweets(tweet._json['source'])

for tweet in tweets:
	filtered_tweet = clean_tweets(tweet._json['text'])
	print(filtered_tweet)
	sentiment = sentiment_analysis(filtered_tweet)
	print(sentiment)
	add_tweet(filtered_tweet, sentiment)


def create_csv_file():
	# with open('news.csv', 'w') as csvfile: 
	with open('news.csv', 'w') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=',', 
										quotechar='|', 
										quoting=csv.QUOTE_MINIMAL)  
		filewriter.writerow(['id', 'created_at', 'clean_text', 'source', 'sentiment']) 


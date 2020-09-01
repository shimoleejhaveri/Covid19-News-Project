'''Create model based the Tweet data and save it'''

import csv 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

# loading data
data = pd.read_csv('tweet.csv', delimiter='|', names = ['id', 'published_at', 'text', 'sentiment']) 
df = pd.DataFrame(data)
df1 = df[['text', 'sentiment']].copy()

# Remove missing values (NaN)
df1 = df1[pd.notnull(df1['sentiment'])]

# Percentage of sentiments with text
total = df1['sentiment'].notnull().sum()
round((total/len(df)*100),1)

pd.DataFrame(df.sentiment.unique()).values

# Create a new column 'category_id' with encoded categories 
df1['category_id'] = df1['sentiment'].factorize()[0]
category_id_df = df1[['sentiment', 'category_id']].drop_duplicates()

# Dictionaries for future use
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'sentiment']].values)

#####Pre-processing
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5,
                        ngram_range=(1, 2), 
                        stop_words='english')

# Transform each text into a vector
features = tfidf.fit_transform(df1.text.values.astype('U')).toarray()
labels = df1.category_id
  
# multi-classification model
X = df1['text'] # Collection of documents
y = df1['sentiment'] # Target or the labels we want to predict (i.e., the 3 different sentiments)

# Model creation
X_train, X_test, y_train, y_test,indices_train,indices_test = train_test_split(features, 
                                                               labels, 
                                                               df1.index, test_size=0.25, 
                                                               random_state=1)
model = LogisticRegression(random_state=0)
model.fit(X_train, y_train)

# save the model to disk
filename = 'finalized_model.sav'
joblib.dump(model, filename)

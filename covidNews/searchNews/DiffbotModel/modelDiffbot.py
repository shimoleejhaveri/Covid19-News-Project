'''create the model based the Tweet data and save it'''

import os
import csv 
import pandas as pd
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn import metrics
import joblib
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler


# loading data
data = pd.read_csv("diffbotBeforeCorrection.csv", delimiter='|', names = ['published_at', 'text', 'sentiment']) 
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

# test
models = [
# RandomForestClassifier(n_estimators=100, max_depth=5, random_state=0),
LinearSVC(),
MultinomialNB(),
LogisticRegression(random_state=0),
RandomForestClassifier(n_estimators=10),
]

# 5 Cross-validation
CV = 5
cv_df = pd.DataFrame(index=range(CV * len(models)))

entries = []
for model in models:
  model_name = model.__class__.__name__
  accuracies = cross_val_score(model, features, labels, scoring='accuracy', cv=CV)
  for fold_idx, accuracy in enumerate(accuracies):
    entries.append((model_name, fold_idx, accuracy))
    
cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])

# Comparison of model performance
mean_accuracy = cv_df.groupby('model_name').accuracy.mean()
std_accuracy = cv_df.groupby('model_name').accuracy.std()

acc = pd.concat([mean_accuracy, std_accuracy], axis= 1, ignore_index=True)
acc.columns = ['Mean Accuracy', 'Standard deviation']
print(acc)



model = LogisticRegression(random_state=0)
model.fit(X_train, y_train)

# save the model to disk
filename = 'finalized_model5.sav'
joblib.dump(model, filename)

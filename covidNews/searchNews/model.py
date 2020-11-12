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
from imblearn.over_sampling import SMOTE
import pickle


def createModel():
  # Loading data
  data = pd.read_csv("final.csv", delimiter='|', names = ['published_at', 'text', 'sentiment']) 
  df = pd.DataFrame(data)
  df1 = df[['text', 'sentiment']].copy()

  # Remove missing values (NaN)
  df1 = df1[pd.notnull(df1['sentiment'])]

  # Percentage of sentiments with text
  total = df1['sentiment'].notnull().sum()
  round((total/len(df)*100),1)

  pd.DataFrame(df.sentiment.unique()).values

  # Histogram of the data
  number_of_element_per_class = df1['sentiment'].value_counts()

  # Create a new column 'category_id' with encoded categories 
  df1['category_id'] = df1['sentiment'].factorize()[0]
  category_id_df = df1[['sentiment', 'category_id']].drop_duplicates()

  #Pre-processing
  tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5,
                          ngram_range=(1, 2), 
                          stop_words='english')

  # Transform each text into a vector
  features = tfidf.fit_transform(df1.text.values.astype('U')).toarray()
  labels = df1.sentiment

  # Save the vectorizer
  with open('tfidf.pk', 'wb') as fin:
    pickle.dump(tfidf, fin)

  labels_np = labels.to_numpy()
  dict_data = { 'features':list(features), 'label':list(labels_np)}
  dataset = pd.DataFrame(dict_data)
   
  # SMOTE over sampling
  sm = SMOTE()

  # Fit the model to generate the data.
  oversampled_trainX, oversampled_trainY = sm.fit_resample(np.vstack(dataset['features'] ), dataset['label'])
  oversampled_train = pd.concat([pd.DataFrame(oversampled_trainX), pd.DataFrame(oversampled_trainY)], axis=1)

  X = pd.DataFrame(oversampled_trainX)
  Y = pd.DataFrame(oversampled_trainY)
  
  oversampled_train['features']=X.replace('',np.nan).stack().groupby(level=0).apply(list)
  number_of_element_per_class_SMOTE = oversampled_trainY.value_counts()

  # Model creation
  X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, 
                                                      random_state=1)

  # Test
  models = [
  LinearSVC(),
  MultinomialNB(),
  LogisticRegression(random_state=0),
  RandomForestClassifier(n_estimators=10),
  ]

  # 10 Cross-validation
  CV = 10
  cv_df = pd.DataFrame(index=range(CV * len(models)))
  
  entries = []
  for model in models:
    model_name = model.__class__.__name__
    accuracies = cross_val_score(model, oversampled_train['features'], Y, scoring='accuracy', cv=CV)
    print(accuracies)
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
  model.fit(X_train, y_train.values.ravel())

  # Save the model to disk
  filename = 'finalized_model.sav'
  joblib.dump(model, filename)

  # Predict
  y_pred = model.predict(X_test)

  # Checking unique values
  predictions = pd.DataFrame(y_pred)
  print(predictions[0].value_counts())
  print('\t\t\t\tCLASSIFICATIION METRICS\n')
  print(metrics.classification_report(y_test, y_pred, 
                                      target_names= ['positive', 'neutral', 'negative']))

  # Confusion Matrix is a table which rows represent the actual class and columns represents the predicted class.
  conf_mat = confusion_matrix(y_test, y_pred)
  fig, ax = plt.subplots(figsize=(3,3))
  sns.heatmap(conf_mat, annot=True, cmap="Blues", fmt='d',
              xticklabels=category_id_df.sentiment.values, 
              yticklabels=category_id_df.sentiment.values)
  plt.ylabel('Actual')
  plt.xlabel('Predicted')
  plt.title("CONFUSION MATRIX - LinearSVC\n", size=16)
  plt.savefig('cm2.png')

if __name__ == "__main__":
    createModel()

import os
import csv 

import pandas as pd
import numpy as np
from scipy.stats import randint
import seaborn as sns # used for plot interactive graph. 
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
# from IPython.display import display
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn import metrics
#import warnings
#warnings.filterwarnings("ignore", category=FutureWarning)


# loading data
data = pd.read_csv("news.csv", delimiter='|', names = ['Description', 'Content', 'PublishedAt', 'vader_polarity', 'Sentiment_vader', 'blob_polarity', 'Sentiment_blob']) 
df = pd.DataFrame(data)
print(df.shape)
print(df.head(2).T) # Columns are shown in rows for easy reading\
# df = df[pd.notnull(df['Content'])]
df1 = df[['Content', 'Sentiment_blob']].copy()
# Remove missing values (NaN)
df1 = df1[pd.notnull(df1['Sentiment_blob'])]
print(df1.shape)

# Percentage of complaints with text
total = df1['Sentiment_blob'].notnull().sum()
round((total/len(df)*100),1)
print(round((total/len(df)*100),1))

pd.DataFrame(df.Sentiment_blob.unique()).values
print(pd.DataFrame(df.Sentiment_blob.unique()).values)

# Create a new column 'category_id' with encoded categories 
df1['category_id'] = df1['Sentiment_blob'].factorize()[0]
category_id_df = df1[['Sentiment_blob', 'category_id']].drop_duplicates()


# Dictionaries for future use
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'Sentiment_blob']].values)

# New dataframe
print(df1.head())


plt.style.use('classic')
fig = plt.figure(figsize=(4,6))
colors = ['grey','grey','grey','grey','grey','grey','grey','grey','grey',
    'grey','darkblue','darkblue','darkblue']
df1.groupby('Sentiment_blob').Content.count().sort_values().plot.barh(
    ylim=0, color=colors, title= 'NUMBER OF COMPLAINTS IN EACH sentiment CATEGORY\n')
plt.xlabel('Number of ocurrences', fontsize = 10);
# plt.savefig('foo.png')
plt.show()


######################Pr-processing
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5,
                        ngram_range=(1, 2), 
                        stop_words='english')

# We transform each complaint into a vector
features = tfidf.fit_transform(df1.Content.values.astype('U')).toarray()

labels = df1.category_id

print("Each of the %d complaints is represented by %d features (TF-IDF score of unigrams and bigrams)" %(features.shape))


# Finding the three most correlated terms with each of the product categories
N = 5
for Sentiment_blob, category_id in sorted(category_to_id.items()):
  features_chi2 = chi2(features, labels == category_id)
  indices = np.argsort(features_chi2[0])
  feature_names = np.array(tfidf.get_feature_names())[indices]
  unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
  bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
  print("\n==> %s:" %(Sentiment_blob))
  print("  * Most Correlated Unigrams are: %s" %(', '.join(unigrams[-N:])))
  print("  * Most Correlated Bigrams are: %s" %(', '.join(bigrams[-N:])))


# multi-classification model
X = df1['Content'] # Collection of documents
y = df1['Sentiment_blob'] # Target or the labels we want to predict (i.e., the 3 different sentiments)

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.25,
                                                    random_state = 0)

models = [
    RandomForestClassifier(n_estimators=100, max_depth=5, random_state=0),
    LinearSVC(),
    MultinomialNB(),
    LogisticRegression(random_state=0),
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

acc = pd.concat([mean_accuracy, std_accuracy], axis= 1, 
          ignore_index=True)
acc.columns = ['Mean Accuracy', 'Standard deviation']
print(acc)





plt.figure(figsize=(8,5))
sns.boxplot(x='model_name', y='accuracy', 
            data=cv_df, 
            color='lightblue', 
            showmeans=True)
plt.title("MEAN ACCURACY (cv = 5)\n", size=14)
# plt.savefig('aa.png')

# Model Evaluation
X_train, X_test, y_train, y_test,indices_train,indices_test = train_test_split(features, 
                                                               labels, 
                                                               df1.index, test_size=0.25, 
                                                               random_state=1)
model = LinearSVC()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print( [df1['Sentiment_blob'].unique()])
# Classification report
print('\t\t\t\tCLASSIFICATIION METRICS\n')
print(metrics.classification_report(y_test, y_pred, 
                                    target_names= [ 'positive', 'neutral', 'negative']))


# A Confusion Matrix is a table which rows represent the actual class and columns represents the predicted class.
conf_mat = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(3,3))
sns.heatmap(conf_mat, annot=True, cmap="Blues", fmt='d',
            xticklabels=category_id_df.Sentiment_blob.values, 
            yticklabels=category_id_df.Sentiment_blob.values)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title("CONFUSION MATRIX - LinearSVC\n", size=16)

# plt.savefig('cm.png')


# # Let’s have a look at the cases that were wrongly classified.
# for predicted in category_id_df.category_id:
#   for actual in category_id_df.category_id:
#     if predicted != actual and conf_mat[actual, predicted] >= 20:
#       print("'{}' predicted as '{}' : {} examples.".format(id_to_category[actual], 
#                                                            id_to_category[predicted], 
#                                                            conf_mat[actual, predicted]))
    
#       display(df1.loc[indices_test[(y_test == actual) & (y_pred == predicted)]][['Sentiment_blob','Content']])
#       print('')





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


def createModel():
    # loading data
    data = pd.read_csv("diffbotFinal22.csv", delimiter='||', names = ['published_at', 'text', 'sentiment']) 
    print(data.sentiment.value_counts())
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
                            ngram_range=(1, 3), 
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



    from collections import Counter
    from sklearn.metrics import accuracy_score, precision_score
    from sklearn.tree import DecisionTreeClassifier

# try oversampling with SMOTE and ADASYN : the accurancy was not good
    from imblearn.over_sampling import SMOTE, ADASYN
    from imblearn.over_sampling import BorderlineSMOTE, SVMSMOTE
    from imblearn.combine import SMOTETomek

    from imblearn.pipeline import Pipeline
    from imblearn.over_sampling import SMOTE
    from imblearn.under_sampling import RandomUnderSampler
    from sklearn.model_selection import cross_val_score
    from sklearn.model_selection import RepeatedStratifiedKFold
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.decomposition import PCA

    from imblearn.over_sampling import RandomOverSampler






    from imblearn.under_sampling import TomekLinks, RandomUnderSampler

    from imblearn.under_sampling import ClusterCentroids


    
# 0.5
    # bc = RandomUnderSampler(random_state=0)
    # X_resampled, y_resampled = bc.fit_sample(X_train, y_train)
    # model = LogisticRegression(random_state=0)
    # model.fit(X_resampled, y_resampled)
    # rfc_pred = model.predict(X_test)
    # print(sorted(Counter(y_resampled).items()))
    # print(accuracy_score(y_test, rfc_pred))
    # print(precision_score(y_test, rfc_pred, average='weighted'))



# 0.5
    # cc = SMOTETomek(sampling_strategy='auto')
    # X_resampled, y_resampled = cc.fit_sample(X_train, y_train)
    # model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
    # model.fit(X_resampled, y_resampled)
    # rfc_pred = model.predict(X_test)
    # print(accuracy_score(y_test, rfc_pred))
    # print(precision_score(y_test, rfc_pred, average='weighted'))


    # # define model: 0.5714285714285714
    # mm = PCA(n_components=3)
    # mm.fit_transform(X_train)
    # model = LogisticRegression(random_state=0)
    # model.fit(X_train, y_train)
    # rfc_pred = model.predict(X_test)
    # print(accuracy_score(y_test, rfc_pred))
    # print(precision_score(y_test, rfc_pred, average='weighted'))



# # 0.5333333333333334
    # X_resampled, y_resampled = SVMSMOTE(sampling_strategy='auto', k_neighbors=5, m_neighbors=5).fit_resample(X_train, y_train)
    # print(sorted(Counter(y_resampled).items()))
    # model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
    # # DecisionTreeClassifier()
    # # LinearSVC()
    # # RandomForestClassifier(n_estimators=100, max_depth=5, random_state=0)RandomForestClassifier(n_estimators=100, max_depth=5, random_state=0)
    # # LogisticRegression(random_state=0)
    # model.fit(X_resampled, y_resampled)
    # rfc_pred = model.predict(X_test)
    # print(accuracy_score(y_test, rfc_pred))
    # print(precision_score(y_test, rfc_pred, average='weighted'))
















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
    # plt.savefig('aa2.png')

    # Model Evaluation
    X_train, X_test, y_train, y_test,indices_train,indices_test = train_test_split(features, 
                                                                   labels, 
                                                                   df1.index, test_size=0.25, 
                                                                   random_state=1)
    


    model = RandomForestClassifier(n_estimators=10)
    # LogisticRegression(random_state=0)
    # MultinomialNB()
    # RandomForestClassifier(n_estimators=100, max_depth=5, random_state=0) -- 0 recall and precision
    # LinearSVC()
    # LogisticRegression(random_state=0)
    

    model.fit(X_train, y_train)

    # save the model to disk
    filename = 'finalized_model.sav'
    joblib.dump(model, filename)

    # predict
    y_pred = model.predict(X_test)

    # Checking unique values
    predictions = pd.DataFrame(y_pred)
    print(predictions[0].value_counts())
    # print( [df1['sentiment'].unique()])
    # Classification report
    print('\t\t\t\tCLASSIFICATIION METRICS\n')
    print(metrics.classification_report(y_test, y_pred, 
                                        target_names= ['positive', 'neutral', 'negative']))


    # A Confusion Matrix is a table which rows represent the actual class and columns represents the predicted class.
    conf_mat = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(3,3))
    sns.heatmap(conf_mat, annot=True, cmap="Blues", fmt='d',
                xticklabels=category_id_df.sentiment.values, 
                yticklabels=category_id_df.sentiment.values)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title("CONFUSION MATRIX - LinearSVC\n", size=16)
    # 
    plt.savefig('cm2.png')

    model = LogisticRegression(random_state=0)
    model.fit(X_train, y_train)

    # save the model to disk
    filename = 'finalized_model2.sav'
    joblib.dump(model, filename)


if __name__ == "__main__":
    createModel()


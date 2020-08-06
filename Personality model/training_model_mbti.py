# importing packages

import pickle
import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string 
from sklearn.metrics import accuracy_score
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.decomposition import TruncatedSVD
from imblearn.over_sampling import SMOTE
# from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import GridSearchCV
from imblearn.metrics import  classification_report_imbalanced 
from imblearn.under_sampling import RandomUnderSampler
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from imblearn.pipeline import make_pipeline as make_pipeline_imb


# Reading dataset 

df_working=pd.read_csv('datasets/preprocessed_dataset/mbti_preprocessed.csv')

# Create a binary column for each of the 4 axis types for later analysis
df_working['I-E'] = df_working['type'].map(lambda x: 'Introversion' if x[0] == 'I' else 'Extroversion')
df_working['N-S'] = df_working['type'].map(lambda x: 'Intuition' if x[1] == 'N' else 'Sensing')
df_working['T-F'] = df_working['type'].map(lambda x: 'Thinking' if x[2] == 'T' else 'Feeling')
df_working['J-P'] = df_working['type'].map(lambda x: 'Judging' if x[3] == 'J' else 'Perceiving')

df_working.head()


# Add to the stopwords list each of the 16 codes
types = ['infj', 'entp', 'intp', 'intj', 'entj', 'enfj', 'infp', 'enfp', 'isfp', \
         'istp', 'isfj', 'istj', 'estp', 'esfp', 'estj', 'esfj']
stop = stopwords.words('english')

for type in types:
    stop.append(type)

stop_rev = stop    
# print(stop_rev)

# Cleaning text 
def cleaner(text):
    stemmer = PorterStemmer()                                        # replaces post separators with empty space
    text = re.sub(r'\bhttps?:\/\/.*?[\d\r\n\|\{\}\(\)\'\"\\/]*? ', 'URL ', text, flags=re.MULTILINE)  # replace hyperlink with 'URL'
    text = text.translate(str.maketrans('', '', string.punctuation)) # removes punctuation
    text = text.translate(str.maketrans('', '', string.digits))      # removes digits
    text = text.lower().strip()                                      # convert to lower case
    final_text = []
    for w in text.split():
        if w not in stop:
            final_text.append(stemmer.stem(w.strip()))
    return ' '.join(final_text)
	
# separating each label 
	
# Train-test splits, using type variables as target and posts variable as predictor
# Introversion - Extroversion
X_train_IE, X_test_IE, y_train_IE, y_test_IE = train_test_split(df_working['posts'].values,
                                                   df_working['I-E'].values,
                                                   test_size=0.30, random_state=42)
# Intuition - Sensing
X_train_NS, X_test_NS, y_train_NS, y_test_NS = train_test_split(df_working['posts'].values,
                                                   df_working['N-S'].values,
                                                   test_size=0.30, random_state=42)
# # Thinking - Feeling
X_train_TF, X_test_TF, y_train_TF, y_test_TF = train_test_split(df_working['posts'].values,
                                                   df_working['T-F'].values,
                                                   test_size=0.30, random_state=42)
# # Judging - Perceiving
X_train_JP, X_test_JP, y_train_JP, y_test_JP = train_test_split(df_working['posts'].values,
                                                   df_working['J-P'].values,
                                                   test_size=0.30, random_state=42)

# setting up model 


pipe = make_pipeline_imb(TfidfVectorizer(ngram_range=(1,2),norm='l1',max_features=100),
                         RandomUnderSampler(random_state=420),
                         RandomForestClassifier(min_samples_leaf=1, min_samples_split=6, n_estimators=120, 
                             criterion='gini', bootstrap='False', n_jobs= -1))
							 

# training model 


pipe.fit(X_train_JP, y_train_JP)
y_pred = pipe.predict(X_test_JP)
probablity=pipe.predict_proba(X_test_JP)
# Model Accuracy
print("Random forest Accuracy:", accuracy_score(y_test_JP, y_pred))
print(classification_report_imbalanced(y_test_JP, y_pred))

# pickle_out = open("model_f.pickle","wb")
# pickle.dump(pipe, pickle_out)
# pickle_out.close()           
# pipe.fit(X_train, y_train)
# y_pred = pipe.predict(X_test)
#
# # Model Accuracy
# print("Logistic Regression Accuracy:", accuracy_score(y_test, y_pred))
# print(classification_report_imbalanced(y_test, y_pred))
#
# pickle_out = open("model_f.pickle","wb")
# pickle.dump(pipe, pickle_out)
# pickle_out.close()							 
							 
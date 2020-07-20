import pandas as pd
import pickle
from gensim.corpora import Dictionary
import re

# loading glove model for checking valid words 
model=pickle.load(open('glove_model.pkl','rb'))
# loading emotion lexicon file for checking no. of words in user text related with emotions or a garbage texts 
df=pd.read_csv('datasets/preprocessed_dataset/Emotion_Lexicon.csv')
word_list=df.Words.values
def count_word(text):
    """
        Takes text and returns unique texts and words exist in emotion_lexicon file
    """
    global word_list
    words,emotion_lexicon=set(),set()
    text=re.sub('[\W\d]',' ',text).strip().split()
    for word in text:
        try:
            if len(model.get_vector(word)) >0:
                words.add(word)
                if word in word_list:
                    emotion_lexicon.add(word)
        except KeyError:
            print('Not found word : ' ,word)
    return words,emotion_lexicon
	
#words,emotion_lexicon=count_word(input())

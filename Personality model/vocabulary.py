import gensim
import pandas as pd
import os
import re 
import spacy
from gensim.utils import simple_preprocess
from gensim import corpora
import en_core_web_sm
custom_nlp = en_core_web_sm.load()


# In[2]:


#Tag remover funtion
def remove(txt,doc):
    """Removes Tags like \n \t " which is basically a tag defined in language 
        Takes arg1 : tag
        arg2: document of nlp 
        returns doc after removing tag from document 
    """
    try:
        doc=doc.replace(txt,'')
    except:
        txt="\\"+txt
        doc=doc.replace(txt,'')
    return doc

def remove_unwanted_extra(removeable_text_list,doc):
    """
        Takes  arg1 : list which contains user defined stopwords and 
       arg2: document of scipy nlp
       returns document after removing stopwords 
    """
    try:
        for txt in removeable_text_list:
            doc=remove(txt,doc)
    except Exception as e:
        print(e)
        return 
    return doc
  
# lemmatization 
def lemmatize(doc):
    """
        Takes doc of scipy nlp and returns lemmatix=zed words 
    """
    return list(set(token.lemma_ for  token in doc))
# remove Unwanted things from nlp object
def remove_unwanted(doc):
    words=list(set(token for token in doc if not token.is_stop and len(token.text)>2 and not token.is_space and not token.text.isdigit() and not token.is_punct and not token.is_bracket and not token.is_quote and not token.like_url and not token.like_num and not token.like_email and any([str(i) in ['a','e','i','o','u'] for i in token.text]) ))
    return lemmatize(words)
# file line iterator 
def file_line(df,column_name):
    for line in df[colummn_name]:
        yield line


# In[11]:


def clean(text):
    """
        From text removing all int/float and stopwords , tag texts , user defined stopwords and words which is not a valid words according    regular expression and removing single characters 
    """
    un_lst=['\t','\n','\\x']
    text=' '.join(set(remove_unwanted(custom_nlp( re.sub('[\d.,;:\'\"\\!<>@#$%^&?*\(\)\{\}\[\]\=\+\-/`~\|]',' ',remove_unwanted_extra(un_lst,text.lower())) )) ))
    return text

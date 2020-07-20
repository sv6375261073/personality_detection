import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler

class DataPrep():
    def __init__(self):
        self.trait_cat_dict = {
            'O': 'cOPN',
            'C': 'cCON',
            'E': 'cEXT',
            'A': 'cAGR',
            'N': 'cNEU',
            'OPN': 'cOPN',
            'CON': 'cCON',
            'EXT': 'cEXT',
            'AGR': 'cAGR',
            'NEU': 'cNEU',
            'Openness': 'cOPN',
            'Conscientiousness': 'cCON',
            'Extraversion': 'cEXT',
            'Agreeableness': 'cAGR',
            'Neuroticism': 'cNEU'
            }
        self.trait_score_dict = {
            'O': 'sOPN',
            'C': 'sCON',
            'E': 'sEXT',
            'A': 'sAGR',
            'N': 'sNEU',
            'OPN': 'sOPN',
            'CON': 'sCON',
            'EXT': 'sEXT',
            'AGR': 'sAGR',
            'NEU': 'sNEU',
            'Openness': 'sOPN',
            'Conscientiousness': 'sCON',
            'Extraversion': 'sEXT',
            'Agreeableness': 'sAGR',
            'Neuroticism': 'sNEU'
            }
        self.LIWC_features = [
            'WPS', 'Unique', 'Dic', 'Sixltr', 'Negate', 'Assent', 'Article', 'Preps', 'Number',
            'Pronoun', 'I', 'We', 'Self', 'You', 'Other',
            'Affect', 'Posemo', 'Posfeel', 'Optim', 'Negemo', 'Anx', 'Anger', 'Sad',
            'Cogmech', 'Cause', 'Insight', 'Discrep', 'Inhib', 'Tentat', 'Certain',
            'Senses', 'See', 'Hear', 'Feel',
            'Social', 'Comm', 'Othref', 'Friends', 'Family', 'Humans',
            'Time', 'Past', 'Present', 'Future',
            'Space', 'Up', 'Down', 'Incl', 'Excl', 'Motion',
            'Occup', 'School', 'Job', 'Achieve',
            'Leisure', 'Home', 'Sports', 'TV', 'Music',
            'Money',
            'Metaph', 'Relig', 'Death', 'Physcal', 'Body', 'Sexual', 'Eating', 'Sleep', 'Groom',
            'Allpct', 'Period', 'Comma', 'Colon', 'Semic', 'Qmark', 'Exclam', 'Dash', 'Quote', 'Apostro', 'Parenth', 'Otherp',
            'Swear', 'Nonfl', 'Fillers',
        ]
        self.tfidf = TfidfVectorizer(stop_words='english', strip_accents='ascii')
    def transform(self,X):
        """
        Takes raw_text( ['hi i am ok '] ) and converts raw_texts into vector and return vectors  
        """
        X = self.tfidf.fit_transform(X)
        return X
    def prep_data(self, type, trait, regression=False, model_comparison=False):
        """
        Conversion of text to vector of document type of text 
        """
        df_status = self.prep_status_data()
        # df_essay = self.prep_essay_data()

        tfidf = TfidfVectorizer(stop_words='english', strip_accents='ascii')

        if type == 'essay':

            # result = tfidf.fit_transform(df_essay['TEXT']).todense()
            #
            # scaler = MinMaxScaler()
            # other_features_df = scaler.fit(df_essay[self.LIWC_features])
            #
            # X = np.nan_to_num(np.column_stack((result, )))

            # If need data to compare models
            if model_comparison:
                X = tfidf.fit_transform(df_essay['TEXT'])
            # Data for fitting production model
            else:
                X = df_essay['TEXT']

            y_column = self.trait_cat_dict[trait]
            y = df_essay[y_column]

        elif type == 'status':
            # Include other features with tfidf vector
            other_features_columns = [
                'NETWORKSIZE',
                'BETWEENNESS',
                'NBETWEENNESS',
                'DENSITY',
                'BROKERAGE',
                'NBROKERAGE',
                'TRANSITIVITY'
            ]
            # result = tfidf.fit_transform(df_status['STATUS']).todense()

            # If need data to compare models
            if model_comparison:
                X = tfidf.fit_transform(df_status['STATUS'])
                # X = np.nan_to_num(np.column_stack((result, df_status[other_features_columns])))
            # Data to fit production model
            else:
                X = df_status['STATUS']

            if regression:
                y_column = self.trait_score_dict[trait]
            else:
                y_column = self.trait_cat_dict[trait]
            y = df_status[y_column]

        return X, y


    def prep_status_data(self):
        """"
        Label conversion into boolian type 0/1 of personality data
        """
        df = pd.read_csv('datasets/preprocessed_dataset/mypersonality_final.csv', encoding="ISO-8859-1")
        df = self.convert_traits_to_boolean(df)
        return df

     #preprocessing essay and mairesse datasets 
    def prep_essay_data(self):
        """"
        Reading Essay.csv and mairesse.csv , concating them and converting their labels into boolian form , returns a single dataset df
        """
        df_essays = pd.read_csv('datasets/preprocessed_dataset/essays.csv', encoding="ISO-8859-1")
        df_mairesse = pd.read_csv('datasets/preprocessed_dataset/mairesse.csv', encoding="ISO-8859-1", header=None)


        df_mairesse.columns = ['#AUTHID'] + self.LIWC_features

        df = df_essays.merge(df_mairesse, how = 'inner', on = ['#AUTHID'])

        # add word count (WC) column
        df['WC'] = df['TEXT'].str.split().str.len()

        df = self.convert_traits_to_boolean(df)

        return df
    # mapping traits in yes/No form 
    def convert_traits_to_boolean(self, df):
        """
        Boolian conversion of labels of each 5 traits , returns a converted dataset of label into boolian form 
        """
        trait_columns = ['cOPN', 'cCON', 'cEXT', 'cAGR', 'cNEU']
        d = {'y': True, 'n': False}

        for trait in trait_columns:
            df[trait] = df[trait].map(d)

        return df

    # loading dataset 
    def load_data(self, filepath):
        """
        Takes path of the csv file and read that , returns dataset object 
        """
        return pd.read_csv(filepath, encoding="ISO-8859-1")

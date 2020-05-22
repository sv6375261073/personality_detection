import pickle
import os
import pandas as pd
from math import pi
from model import Model
from data_prep import DataPrep

# loading cat_5 models 
class Predictor_cat5():
    def __init__(self):
        self.traits = ['OPN', 'CON', 'EXT', 'AGR', 'NEU']
        self.categories=['OPENNESS','CONSCIENTIOUSNESS','EXTRAVERSION','AGREEABLENESS','NEUROTICISM']
        self.Pre_cat = {trait:cat for (trait,cat) in zip(self.traits,self.categories)}
        self.models={trait:pickle.load(open('static/'+trait+'_model.pkl', 'rb')) for i,trait in enumerate(self.traits)}
        self.dp=DataPrep()
    def predict(self, X, traits='All', predictions='All'):
        predictions = {}
        self.dp.transform(X)
        if traits == 'All':
            for trait in self.traits:
                pkl_model = self.models[trait]
                # trait_categories = pkl_model.predict(X, regression=False)
                # predictions[self.Pre_cat[trait]+'  '] = str(trait_categories[0])
                # trait_scores = pkl_model.predict(X, regression=True).reshape(1, -1)
                # predictions[self.Pre_cat[trait]+'  '] = predictions[self.Pre_cat[trait]+'  ']+' '+str(round(trait_scores.flatten()[0]*10))+' % '
                trait_categories_probs = pkl_model.predict_proba(X)
                predictions[self.Pre_cat[trait]+'  '] = trait_categories_probs[:, 1][0]*100
        return predictions

# loading mbti models
class mbti_models:
    def __init__(self):
        self.traits=['IE','NS','TF','JP']
        self.models={trait+'_model':pickle.load(open('static/rfc_'+trait+'_model.pkl','rb')) for trait in self.traits}
    def predict(self,text):
        categories=[('Introversion','Extroversion'),('Intution','Sensing'),('Thinking','Feeling'),('judging','perceving')]
        self.prediction,self.probablity={},{}
        for i,trait in enumerate(self.traits):
#             self.prediction[trait]=self.models[trait+'_model'].predict(text)[0] 
            self.probablity[categories[i][0]],self.probablity[categories[i][1]]=list(self.models[trait+'_model'].predict_proba(text)[0]*100) 
        return self.probablity

# ibject of mbti model
model=mbti_models()
#object of cat_5 model 
p_cat5=Predictor_cat5()

# taking input for prediction
text=[input(" Enter text : ")]

probablity=model.predict(text)
prediction_cat5=p_cat5.predict(text)
probablity.update(prediction_cat5)
print(probablity)
import pickle
import os
class models:
    def __init__(self):
        self.traits=['IE','NS','TF','JP']
        self.models={trait+'_model':pickle.load(open('static/'+'rfc_'+trait+'_model.pkl','rb')) for trait in self.traits}
    def predict(self,text):
        self.prediction_text={trait:self.models[trait+'_model'].predict(text) for trait in self.traits}

        self.prediction={trait:self.models[trait+'_model'].predict(text)[0] for trait in self.traits}
        self.probablity={trait:self.models[trait+'_model'].predict_proba(text)[0] for trait in self.traits}
        return self.prediction,self.probablity,self.prediction_text

# model=models()
# prediction,probablity=model.predict([input(" Enter text : ")])
# traits=[('Introversion','Extroversion'),('Intution','Sensing'),('Thinking','Feeling'),('judging','perceving')]
# for i,j,k in zip(traits,prediction.values(),probablity.values()):
#     print('\n_________________________******************************_____________________________\n')
#     print(f' Traits: {i} ,__Text_prediction : {j}, __probablity_of_traits : {k}')
#     print()

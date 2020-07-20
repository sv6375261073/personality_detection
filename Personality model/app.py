from flask  import Flask,request,jsonify  # for flask app , requesting server and jsonify data
from model import Model    # importng model from  created module
import tensorflow as tf
import keras
from update_personality import update_prediction  # for updatating prediction based on user review 
from words_in_emotionLexicon import count_word    # for counting required word of emotions in user text 
from vocabulary import clean                      # preprocessing text 
#import tensorflow_core.keras
from prediction import Predictor_cat5,mbti_models # importing all prediction function of models 
app=Flask(__name__)
Predictor_cat5_obj,mbti_models_obj=Predictor_cat5(),mbti_models() # creating objects 
model=Model()
probablity={}          # creting dictionary of personality trades                       
@app.route('/',methods=['POST'])
def test(): 
    """
        It takes text in json format by post methot and returns probablity of 5 traits dictionary form 
    """
    # getting text from user using post methot and predicting user personality 
    global probablity
    if request.method=='POST': 
        json_data=request.json # taking json data from post method 
        text=json_data['text'] # exteracting text 
        text=clean(text)       # cleaning text
        words,lex_words=count_word(text) # counting required words 
        if len(lex_words)<50:    # if user text is not proper to the model 
            return  jsonify({'warning':'Not enough required words'}) 
        else:   # if tet fulfills requirement for good texts , returns personality values 
            cat5_probablity=Predictor_cat5_obj.predict([text])
            mbti_probablity=mbti_models_obj.predict([text])
            probablity.update(cat5_probablity)
            probablity.update(mbti_probablity)
            return jsonify({'probablities':str(probablity)})

@app.route('/review',methods=['POST'])
def update_personality_trades(): # updating personality by getting review of user 
    """
        It takes review in integer form from user as feedback and this function will return updated personlity with review in dictionary form
    """
    if request.method=='POST':
        json_data=request.json          # taking json data of user review in integer type 
        review=json_data['review']        # review of user 
        probablity=update_prediction(probablity,review)
        return jsonify({'probablities':str(probablity)})        # returning json data
if __name__=='__main__':
    app.run(debug=True,port=9090)
        

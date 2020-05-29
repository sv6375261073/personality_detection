from flask  import Flask,request,jsonify
from model import Model
import tensorflow as tf
import keras
from update_personality import update_prediction
from words_in_emotionLexicon import count_word
from vocabulary import clean 
#import tensorflow_core.keras
from prediction import Predictor_cat5,mbti_models
app=Flask(__name__)
Predictor_cat5_obj,mbti_models_obj=Predictor_cat5(),mbti_models()
model=Model()
probablity={}
@app.route('/',methods=['POST'])
def test():
    global probablity
    if request.method=='POST':
        json_data=request.json
        text=json_data['text']
        text=clean(text)
        words,lex_words=count_word(text)
        if len(lex_words)<50:
            return  jsonify({'warning':'Not enough required words'}) 
        else:
            cat5_probablity=Predictor_cat5_obj.predict([text])
            mbti_probablity=mbti_models_obj.predict([text])
            probablity.update(cat5_probablity)
            probablity.update(mbti_probablity)
            return jsonify({'probablities':str(probablity)})

@app.route('/review',methods=['POST'])
def update_personality_trades():
    if request.method=='POST':
        json_data=request.json
        review=json_data['review']
        probablity=update_prediction(probablity,review)
        return jsonify({'probablities':str(probablity)})        
if __name__=='__main__':
    app.run(debug=True,port=9090)
        
from flask  import Flask,request,jsonify
from model import Model
import tensorflow as tf
import keras
#import tensorflow_core.keras
from prediction import Predictor_cat5,mbti_models
app=Flask(__name__)
Predictor_cat5_obj,mbti_models_obj=Predictor_cat5(),mbti_models()
model=Model()
@app.route('/',methods=['POST'])
def test():
    probablity={}
    if request.method=='POST':
        json_data=request.json
        text=json_data['text']
        cat5_probablity=Predictor_cat5_obj.predict([text])
        mbti_probablity=mbti_models_obj.predict([text])
        probablity.update(cat5_probablity)
        probablity.update(mbti_probablity)
        return jsonify({'probablities':str(probablity)})
        
if __name__=='__main__':
    app.run(debug=True,port=9090)
        

import flask
from flask import request, jsonify

import pandas as pd
from math import pi
from model import Model
from data_prep import DataPrep
from prediction_class import models
from prediction import mbti_models,Predictor_cat5

app = flask.Flask(_name_)
app.config["DEBUG"] = True

models=models()
@app.route('/', methods=['GET'])


def home():
	global models
	prediction1,probablity1,prediction_text=models.predict(main_text)
	#print("main_ presonality",prediction1)
	model=mbti_models()
	# object of cat_5 model 
	p_cat5=Predictor_cat5()
    json_data=request.json
    text=json_data['text']
	probablity=model.predict(main_text)
	prediction_cat5=p_cat5.predict(main_text)
	book = {'Personality_of_character % ':probablity,'Big_five presonality % ':prediction_cat5,"Personality_of_character":prediction1}
	return jsonify(book)




if _name_ == '_main_':
    app.run(debug=True,port = 8000)
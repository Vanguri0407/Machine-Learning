import numpy as np
from flask import Flask, request, jsonify, render_template, make_response
import pickle
from flask_cors import cross_origin
import json
import os

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='Employee Salary should be $ {}'.format(output))
@app.route('/predictsalary',methods=['POST'])
@cross_origin()
def predictsalary():
    '''
    For rendering results to DialogFlow
    '''
    req = request.get_json(silent=True, force=True)

    sessionID=req.get('responseId')


    result = req.get("queryResult")
    user_says=result.get("queryText")
    #log.write_log(sessionID, "User Says: "+user_says)
    parameters = result.get("parameters")
    interview_score=parameters.get("interview_score")
    #print(cust_name)
    test_score = parameters.get("test_score")
    experience=parameters.get("experience")
    #course_name= parameters.get("course_name")
    
    
    int_features = [interview_score,test_score,experience]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)
    res = { "fulfillmentText" : "Your predicted Salary is $ {}format(output)  }
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

if __name__ == "__main__":
    app.run(debug=True)

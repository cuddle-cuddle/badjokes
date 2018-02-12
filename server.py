import os
import pandas as pd
import dill as pickle
from flask import Flask, jsonify, request
from utils import PreProcessing
import json

app = Flask(__name__)

global loaded_model
clf = 'model_v1.pk'
model_path = '../flask_api/models/'+clf
#Load the saved model
print("Loading the model...")
loaded_model = None
with open(model_path,'rb') as f:
    loaded_model = pickle.load(f)
print("model loaded")

@app.route('/predict', methods=['POST'])
def apicall():
    """API Call
    
    Pandas dataframe (sent as a payload) from API Call
    """
    print("API call received")    
    try:
        test_json = request.get_json()
        print('json read:')
        print(test_json)
        #d = json.loads(str(test_json))
        #print('getting d')
        #test = pd.DataFrame.from_dict(d, orient='index').T
        #test = pd.read_json(test_json, orient='records')
        test = pd.DataFrame.from_dict(test_json, orient='index').T
        print("json turned into pd")
        
        #To resolve the issue of TypeError: Cannot compare types 'ndarray(dtype=int64)' and 'str'
        test['Dependents'] = [str(x) for x in list(test['Dependents'])]
        print('parsing dependents')
        
        #Getting the Loan_IDs separated out
        loan_ids = test['Loan_ID']

    except Exception as e:
        raise e
    
    clf = 'model_v1.pk'
    model_path = '../flask_api/models/'+clf
    
    if test.empty:
        return(bad_request())
    else:
        #Load the saved model
        print("Loading the model...")
        #loaded_model = None
        #with open(model_path,'rb') as f:
    #        loaded_model = pickle.load(f)

        print("The model has been loaded...doing predictions now...")
        predictions = loaded_model.predict(test)
        print("predictions are calcuated. ")
        
        """Add the predictions as Series to a new pandas dataframe
                                OR
           Depending on the use-case, the entire test data appended with the new files
        """
        prediction_series = list(pd.Series(predictions))
        print("got predicitons series")

        final_predictions = pd.DataFrame(list(zip(loan_ids, prediction_series)))
        print("made final predicitons")
        
        """We can be as creative in sending the responses.
           But we need to send the response codes as well.
        """
        responses = jsonify(predictions=final_predictions.to_json(orient="records"))
        responses.status_code = 200

        return (responses)


@app.errorhandler(400)
def bad_request(error=None):
    message = {
            'status': 400,
            'message': 'Bad Request: ' + request.url + '--> Please check your data payload...',
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp
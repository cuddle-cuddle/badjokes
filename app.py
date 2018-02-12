
# coding: utf-8

# In[1]:


import os
from flask import Flask, jsonify, request
from jokesModel import *


# In[2]:


app = Flask(__name__)


# In[5]:


def getJSONResult(req):
    result = req.get("result")
    
    if result is None: 
        print('result not found. ')
        return {}
    
    intent = result.get("metadata").get("intentName")
    parameters = result.get("parameters")
    
    if intent == 'match_kids_jokes':
        text = parameters.get("search_text")
        s = "Search " + text + ":"
        results = getMatchingJokesJSON(text)
        return {
            "speech": s,
            "displayText": s,
            "data": results
        }


# In[6]:



@app.route('/predict', methods=['POST'])
def apicall():
    """API Call
    """
    print("API call received")  
    
    try:
        req = request.get_json(silent=True, force=True)
        print('request received')
        response = getJSONResult(req)
        print('results are parsed')
        print(response)
        return jsonify(response)
    
    except Exception as e:
        raise e
        message = {
            'message': 'error retrieving jokes'
        }


@app.errorhandler(400)
def bad_request(error=None):
    message = {
            'status': 400,
            'message': 'Bad Request: ' + request.url + '--> Please check your data payload...',
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp


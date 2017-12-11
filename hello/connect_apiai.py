import os.path

import sys
import json
import views

import pymysql
from random import choice
import random

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = 'c11136b7965143f582328de10df34835'

def get_apiai(message):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'en'  # optional, default value equal 'en'

    request.query = message

    response = request.getresponse()
    responsestr = response.read().decode('utf-8')
    response_obj = json.loads(responsestr)
    
    if response_obj["result"]["source"] == 'domains':
        return response_obj["result"]["fulfillment"]["speech"]
    
    elif response_obj["result"]["metadata"]["intentName"] == 'wholerandom':
        return "How about " + response_obj["result"]["fulfillment"]["speech"] + "?"
        
    elif response_obj["result"]["metadata"]["intentName"] == 'signature':
        rst = views.branddb(response_obj["result"]["parameters"]["brand"])
        return rst
    
    elif response_obj["result"]["metadata"]["intentName"] == 'condition':
        rst = views.updatedb(response_obj["result"]["parameters"]["amount"], response_obj["result"]["parameters"]["taste"], response_obj["result"]["parameters"]["number"], response_obj["result"]["parameters"]["alone"],
        response_obj["result"]["parameters"]["meat"], response_obj["result"]["parameters"]["noodle"], response_obj["result"]["parameters"]["cheap"])
        return rst
    
    #elif response_obj["result"]["sourece"] == 'domains':
    #    return response_obj["result"]["fulfillment"]["messages"]["speech"]
    
    else:
        return response_obj["result"]["fulfillment"]["speech"]
    
#def get_price(message):
#    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
#    request = ai.text_request()
#    request.lang = 'en'  # optional, default value equal 'en'
#
#    request.query = message
#
#    response = request.getresponse()
#    responsestr = response.read().decode('utf-8')
#    response_obj = json.loads(responsestr)
#    return response_obj["result"]["parameters"]["number"]
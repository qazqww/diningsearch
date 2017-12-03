import os.path

import sys
import json
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
    
    if response_obj["result"]["metadata"]["intentName"] == 'wholerandom':
        return "How about " + response_obj["result"]["fulfillment"]["speech"]
    else:
        return response_obj["result"]["fulfillment"]["speech"]
        
    #["result"]["parameters"]["amount"] == 
    #["result"]["parameters"]["taste"]
    #["result"]["parameters"]["number"]
    
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
    
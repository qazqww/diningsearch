import os.path

import sys
import json

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

Ramount = ''
Rtaste = ''
Rnumber = ''
Ralone = ''

def get_apiai(message):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'en'  # optional, default value equal 'en'

    request.query = message

    response = request.getresponse()
    responsestr = response.read().decode('utf-8')
    response_obj = json.loads(responsestr)
    
    Ramount = response_obj["result"]["parameters"]["amount"]
    Rtaste = response_obj["result"]["parameters"]["taste"]
    Rnumber = response_obj["result"]["parameters"]["number"]
    Ralone = response_obj["result"]["parameters"]["alone"]
    
    if response_obj["result"]["metadata"]["intentName"] == 'wholerandom':
        return "How about " + response_obj["result"]["fulfillment"]["speech"]
    
#    elif Ramount != "" or Rtaste != "" or Rnumber != "" or Ralone != "":
#        #MySQL Connection
#        conn = pymysql.connect(host='127.0.0.1', user='raptarior', password='', db='c9', charset='utf8')
#        #Create Cursor from Connection
#        curs = conn.cursor()
#        
#        #SQL words
#        sql = "SELECT * FROM FOOD WHERE"
#        if Ramount == "light":
#            sql += "amount = 0 and"
#        if Rtaste == "spicy":
#            sql += "spicy = 1 and"
#        if Ralone == "alone":
#            sql += "alone = 1 and"
#        if Rnumber != "":
#            sql += Rnumber + " > price"
#        else:
#            sql += "price <> 0"
#        
#        curs.execute(sql)
#        #data Fetch
#        rows = curs.fetchall()
#        conn.close()
#
#        length = len(rows)
#        i = random.randint(0, length)
#        #menuurl = views.selecturl(rows[i][0])
#        
#        return i
        
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
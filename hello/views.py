from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from .models import Greeting

#added by Jung
from django.views.decorators.csrf import csrf_exempt
import json, datetime
from . import connect_apiai
from .models import Foodlist

# Create your views here.
def index(request):
    foodlists = Foodlist.objects.all()
    str = ''
    for foodlist in foodlists:
        str += "<p>{} {}<br>".format(foodlist.fname, foodlist.price)
    
    return HttpResponse(str)
    # return HttpResponse('Hello from Python!')
    # return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

# added by Jung
def keyboard(request):
   return JsonResponse({
       'type' : 'text'
   })

@csrf_exempt
def message(request):
#    foodlists = Foodlist.objects.all()
#    list1 = []
#    str = ''
#    for foodlist in foodlists:
#        list1.append(foodlist)
#        #str += "<p>{} {}<br>".format(foodlist.fname, foodlist.price)
    
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    content = received_json_data['content']
    today_date = datetime.date.today().strftime("%m %d")
    
    if "man" in content:
        data_will_be_send = {
            'message': {
                'text': "maaaaaaan"
            }
            # ,
            # 'keyboard': {
            #     'type': 'buttons',
            #     'buttons': ['Choose 1', 'Choose 2']
            # }
        }
    elif "hey" in content:
        if connect_apiai.get_apiai(content) > 5000:
            data_will_be_send = {
                'message': {
                    'text': str(int(connect_apiai.get_apiai(content)) - 4000)
                }
            }
        else:
            data_will_be_send = {
                'message': {
                    'text': str(int(connect_apiai.get_apiai(content)) - 4000)
                }
            }
    else:
        data_will_be_send = {
            'message': {
                'text': connect_apiai.get_apiai(content)
            }
        }
        
    return JsonResponse(data_will_be_send)
    
    ######commit please

#@csrf_exempt
#def action(request):
#    json_str = ((request.body).decode('utf-8'))
#    received_json_data = json.loads(json_str)
#    content = received_json_data['content']
#    today_date = datetime.date.today().strftime("%m %d")
#    
#    data_will_be_send = {
#        "speech": "Barack Hussein Obama II was the 44th and current President of the United States.",
#        "displayText": "Barack Hussein Obama II was the 44th and current President of the United States, and the first African American to hold the office. Born in Honolulu, Hawaii, Obama is a graduate of Columbia University   and Harvard Law School, where ",
#        "data": {},
#        "contextOut": [],
#        "source": "DuckDuckGo"
#    }
#    
#    return JsonResponse(data_will_be_send)
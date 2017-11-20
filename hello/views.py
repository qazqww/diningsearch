from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from .models import Greeting

#added by Jung
from django.views.decorators.csrf import csrf_exempt
import json, datetime
from . import connect_apiai

from .models import Foodlist
from random import choice

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
    
    low = ['ramen', 'gimbap', 'flour based food (tteok-bokki, etc.)', 'lunch box']
    lowmid = ['chinese restau.(jajangmyeon, jjamppong, etc.)', 'sandwich', 'gukbap or jjigae', 'hamburger', 
    'bowl of rice', 'lunch box', 'cold noodles', 'donburi', 'rice noodles', 'curry', 'japanese ramen', 'pork cutlet']
    mid = ['pasta', 'sushi', 'hamburger steak', 'fried chicken', 'chicken cuisine(steamed chicken, samgyetang, etc..)'
    , 'cold noodles (of Pyongyang)', 'donburi', 'rice noodles', 'curry', 'japanese ramen', 'pork cutlet']
    high = ['pizza', 'steak', 'jokbal/bossam', 'meat', 'family restaurant', 'buffet', 'raw dishes(sashimi) / seafood'
    , 'shabu-shabu']
    choicemenu = ""
    
    if "man" in content:
        data_will_be_send = {
            'message': {
                'text': "maaaaaaan",
                'photo': {
                    'url': "http://postfiles4.naver.net/MjAxNzEwMjNfMzAw/MDAxNTA4NzU5OTIxNjQ0.Qduj5x9C3tECv_sUoE0BJrTIdR1t9hc_-oCgyTqJchAg.70KA_53h3Eta6PD8gqwOg5W1a4vC_Q6d0z2rZ0mCg-Mg.JPEG.qazqww/1.jpg?type=w2",
                    'width': 640,
                    'height': 480
                    }
                }
            }
            # ,
            # 'keyboard': {
            #     'type': 'buttons',
            #     'buttons': ['Choose 1', 'Choose 2']
            # }
    elif "price" in content:
        if int(connect_apiai.get_apiai(content)) > 12000:
            choicemenu = choice(high)
        elif int(connect_apiai.get_apiai(content)) > 7000:
            choicemenu = choice(mid)
        elif int(connect_apiai.get_apiai(content)) > 4000:
            choicemenu = choice(lowmid)
        else:
            choicemenu = choice(low)
            
        data_will_be_send = {
                'message': {
                'text': "I recommend you to eat " + choicemenu + "."
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
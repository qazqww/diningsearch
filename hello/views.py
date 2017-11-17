from django.shortcuts import render
#from django.http import HttpResponse
from django.http import JsonResponse

from .models import Greeting

#added by Jung
from django.views.decorators.csrf import csrf_exempt
import json, datetime
from . import connect_apiai

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

# added by Jung
def keyboard(request):
    return JsonResponse({
        'type' : 'buttons',
        'buttons' : ['1','2']
        })
 
#   return JsonResponse({
#                 'type' : 'buttons',
#                 'buttons' : ['Choose 1','Choose 2']
#                 })

@csrf_exempt
def message(request):
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    content = received_json_data['content']
    today_date = datetime.date.today().strftime("%m %d")
    
    if "hi" in content:
        data_will_be_send = {
            'message': {
                'text': "hi"
            }
            # ,
            # 'keyboard': {
            #     'type': 'buttons',
            #     'buttons': ['Choose 1', 'Choose 2']
            # }
        }
    else:
        data_will_be_send = {
            'message': {
                'text': connect_apiai.get_apiai(content)
            }

        }
        
    return JsonResponse(data_will_be_send)
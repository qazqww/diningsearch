from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from .models import Greeting

from django.views.decorators.csrf import csrf_exempt
import json, datetime, pymysql, random
from . import connect_apiai

#from .models import Foodlist
from random import choice

##MySQL Connection
#conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='c9', charset='utf8')
##Create Cursor from Connection
#curs = conn.cursor()
#
##SQL words
#sql = "select * from food"
#curs.execute(sql)
#
##data Fetch
#rows = curs.fetchall()
#
#conn.close()

# Create your views here.
def index(request):
    
    # return HttpResponse(rand)
    return HttpResponse('Hello from Python!')
    # return render(request, 'index.html')

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def keyboard(request):
   return JsonResponse({
       'type' : 'text'
   })

@csrf_exempt
def message(request):

    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    content = received_json_data['content']
    today_date = datetime.date.today().strftime("%m %d")
    
    if "ladder" in content:
        data_will_be_send = {
            'message': {
                'text': 'This is a ladder game in Naver site.',
                'photo': {
                  'url': 'http://postfiles2.naver.net/MjAxNzEyMTBfNzQg/MDAxNTEyODg3NjgzMjQz.dvjrBo0XXmyYBfOQv4L49X3kVe7U2CPgYDot_L5eD7wg.RA9OzNfuZm7TKdZxObwahDuB26-Fg2JC6Dd99BoE7_Yg.JPEG.qazqww/222.jpg?type=w2',
                  'width': 640,
                  'height': 480
                },
                'message_button': {
                  'label': 'LADDER GAME',
                  'url': 'https://m.search.naver.com/search.naver?sm=tab_hty&where=nexearch&query=%B3%D7%C0%CC%B9%F6%BB%E7%B4%D9%B8%AE&x=26&y=26'
                }
            }
        }
    
    else:
        selected = connect_apiai.get_apiai(content)
        urlurl = selecturl(selected)

        if urlurl == 'nothing':
            data_will_be_send = {
                'message': {
                    'text': connect_apiai.get_apiai(content)
                }
            }
            
        else:
            data_will_be_send = {
                'message': {
                'text': "I recommend you to eat " + selected + ".",
                'photo': {
                    'url': urlurl,
                    'width': 640,
                    'height': 480
                    }
                }
            }
       
    return JsonResponse(data_will_be_send)
    
    ######commit please
    
    
def updatedb(amount, taste, number, alone, meat, noodle, cheap):

    try:
        conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='c9', charset='utf8')
    except:
        return Exception
   
    #Create Cursor from Connection
    curs = conn.cursor()
   
    #SQL words
    sql = "SELECT * FROM food where"
    if amount == "light":
        sql += " amount = 0 AND"
    elif amount == "substantial":
        sql += " amount = 1 AND"
        
    if taste == "spicy":
        sql += " spicy = 1 AND"
    elif taste == "mild":
        sql += " spicy = 0 AND"
        
    if alone == "alone":
        sql += " alone = 1 AND"
        
    if meat == "meat" and noodle == "noodle":
        " (MEAT = 1 OR noodle = 1)"
    else:
        if meat == "meat":
            sql += " MEAT = 1 AND"
        elif meat == "not meat":
            sql += " MEAT = 0 AND"
        if noodle == "noodle":
            sql += " noodle = 1 AND"
            
    if number != "":
        sql += " price < " + str(number)
    elif cheap != "":
        if cheap == "cheap":
            sql += " price < 4000"
        elif cheap == "expensive":
            sql += " price > 10000"
    #    if number >= 5000:
    #        sql += " AND price > " + str(int(number) - 5000)
    else:
        sql += " price <> 0;"
    
    curs.execute(sql)
    #data Fetch
    rows = curs.fetchall()
    conn.close()
    
    try:
        i = random.randint(0, len(rows)-1)
    except Exception:
        return 'Nothing!'
    
    #menuurl = views.selecturl(rows[i][0])
    
    if len(rows) == 0:
        return 'Nothing!'
    else:
        return rows[i][0]
        
def branddb(name):

    try:
        conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='c9', charset='utf8')
    except:
        return Exception
   
    #Create Cursor from Connection
    curs = conn.cursor()
   
    #SQL words
    sql = "SELECT * FROM best where brand = '" + name + "';"
    
    curs.execute(sql)
    #data Fetch
    rows = curs.fetchall()
    conn.close()
    
    try:
        info = "I think popular menu is " + rows[0][1] + " and price is " + rows[0][2] + "."
    except Exception:
        info = 'Please give me brand name. If you have already done so, it is not in my data, Sorry.'
    
    return info


def selecturl(url):
    
    if url == 'gimbap':
        menuurl = "http://postfiles2.naver.net/MjAxNzExMjBfMTA3/MDAxNTExMTg3MzQ3NjQ0.Pb5aVWbjBKgU0F8EZ8YBJeM4kELi--Q0d2bMO7XPWG8g.cmUSDK0amlYxENy4lPK6bzLbzzaEGW3UYyQtFKVVsXcg.JPEG.qazqww/gimbap.jpg?type=w2"
    elif url == 'japanese ramen':
        menuurl = "http://postfiles15.naver.net/MjAxNzExMjBfNSAg/MDAxNTExMTg3MzQ4NTI0.dwTFe0gp_rvpugSPsmbne1rgrG6f0wtJbGYUJ4OAJ34g.PKcPrVQvxzjL0ReJ0FbeYtx2ixnsRPeA9FV-3XCiwh0g.JPEG.qazqww/jramen.jpg?type=w2"
    elif url == 'hamburger':
        menuurl = "http://postfiles5.naver.net/MjAxNzExMjBfNzkg/MDAxNTExMTg3MzQ5NTE5.3AqmoHH7zE4k1E4XS9_F3OwZjELbOkM5P3-zNYZ3Sfwg.p1iV7glGCOKCVpnXMw3Q_k_gVDEdQh75qxlU11wCdg4g.PNG.qazqww/whopper.png?type=w2"
    elif url == 'sushi':
        menuurl = "http://postfiles15.naver.net/MjAxNzExMjFfMjcw/MDAxNTExMjM4ODAzOTY2.A2LEX8awyMrz7aE7kxJ50yotAruIW5WrU0OdctCPEtog.mA_KCkWu8-X3LyAE2GmNfvgiMNop7ftd0YJkba6xkeog.JPEG.qazqww/sushi.jpg?type=w2"
    elif url == 'ramen':
        menuurl = "http://postfiles2.naver.net/MjAxNzExMjBfMjE5/MDAxNTExMTg3MzQ5MTIy.bIhSvEmClXmzVe3iqNrXVOF9FJM1wPeZQeo2LcR1KT8g.X06R99h23sRZxdu9IPh860HrF7ztgGF42ivS0MxlgeEg.JPEG.qazqww/ramen.jpg?type=w2"
    elif url == 'flour based food (bunsik)':
        menuurl = "http://postfiles14.naver.net/MjAxNzExMjFfMTMw/MDAxNTExMjM3NDU2Nzg5.4sSNCfOPU7duj2iIbgQ3AoWG2foxYYFsjvoHeiiRomUg.qqcqbaAJNAQXdY8g-0k9XFQm2oGEHffipGdk_luTcksg.JPEG.qazqww/1.JPG?type=w2"
    elif url == 'lunch box':
        menuurl = "http://postfiles1.naver.net/MjAxNzExMjFfNzYg/MDAxNTExMjM3NTU3NzQ2.3f39ZE3v9R-7Gm1fWZYxRo3fssDSkstDP5ZZS8-ZA4kg.s_JyphELSkgNGTtOOWvjRzCI00NHS9QUQ2FLinu4Qqgg.JPEG.qazqww/lunchbox.jpg?type=w2"
    elif url == 'jajangmyeon, jjamppong':
        menuurl = "http://postfiles8.naver.net/MjAxNzExMjFfMjU1/MDAxNTExMjM4MDIzNjMx.zk5qx0j2YLdVe8e5hhvs0CGkTZ2F6rLMsiJgu23p0F0g.BIXjqo7kwxa1yNFb-2lGkcc6OPdW97oXAor5n0wd8q0g.PNG.qazqww/chinese.png?type=w2"
    elif url == 'sandwich':
        menuurl = "http://postfiles8.naver.net/MjAxNzExMjFfMTIw/MDAxNTExMjM4MDIzODM2.LkAFE-hwYw0jccwx8JZ6H80fHG81-bwQ6dxxLBQCAPAg.1EaovBbAB1awrRxo3iWy_QypiPeKU102Eq7V9cr0RQYg.JPEG.qazqww/sandwich.jpg?type=w2"
    elif url == 'gukbap':
        menuurl = "http://postfiles2.naver.net/MjAxNzExMjBfMTM1/MDAxNTExMTg3MzQ4MDQw.mgBrer56H1dttKW4s_8k1CF_Fbp5TNT-G-VQZggxxPsg.OXCpnq4Wogw4ng7qEc5iSReEUlX84gqKJZ7Gb6ATNMMg.JPEG.qazqww/jjigae.jpg?type=w2"
    elif url == 'jjigae':
        menuurl = "http://postfiles2.naver.net/MjAxNzExMjBfMTM1/MDAxNTExMTg3MzQ4MDQw.mgBrer56H1dttKW4s_8k1CF_Fbp5TNT-G-VQZggxxPsg.OXCpnq4Wogw4ng7qEc5iSReEUlX84gqKJZ7Gb6ATNMMg.JPEG.qazqww/jjigae.jpg?type=w2"
    elif url == 'bowl of rice':
        menuurl = "http://postfiles13.naver.net/MjAxNzExMjFfNzMg/MDAxNTExMjM4MTE2MzQ1.GO88VdmoRT1vF8L7BA8zZub44bl-3TRfT6EKCykLCVog.3VKvKh8hCm0pjEjZdr4qXWJlTKn_1COXer-xtRssfZwg.JPEG.qazqww/bowl.jpg?type=w2"
    elif url == 'cold noodles':
        menuurl = "http://postfiles16.naver.net/MjAxNzExMjBfMTAx/MDAxNTExMTg3MzQ3MzAw.w3JvoO4uwYa6e6rAb9SlP3Sk55CJTNUl5chf2X8nglUg.wat9NKENg2Nv9zHVgaT3elrJmkpfTmjTnbgdqPzbgskg.JPEG.qazqww/coldnoodles.jpg?type=w2"
    elif url == 'donburi':
        menuurl = "http://postfiles11.naver.net/MjAxNzExMjFfMjcw/MDAxNTExMjM4Mjc3Nzk1.czMM_Rwsl7pk4zLYlyKbsr-AdDfmLjfTGwkjaYR1bjEg.iziwlliP_wQxv2nPEFZbljpEZNdg72X46ClH7IDajcog.JPEG.qazqww/donburi.jpg?type=w2"
    elif url == 'rice noodles':
        menuurl = "http://postfiles16.naver.net/MjAxNzExMjFfNzUg/MDAxNTExMjM4Mjc3OTY4.JDeYNH9OdDXXooC0F96XfrK7gBtUNzGz2mIocd4JK-kg.VXiZp1S_W5u5zdDeUrSd4C6jszn_Yc_a7x4WzWKDmXwg.JPEG.qazqww/ricenoodles.jpg?type=w2"
    elif url == 'curry':
        menuurl = "http://postfiles5.naver.net/MjAxNzExMjBfOTAg/MDAxNTExMTg3MzQ3NTA3.QvdoSxaagzm8XJZRUOx7Aqa57rmcCLWO5sljnu52wBgg.ABi18o7729E1M2ya0veZCpfOQ_dDz4x5r8qNAmdMP7Ag.JPEG.qazqww/curry.jpg?type=w2"
    elif url == 'pork cutlet':
        menuurl = "http://postfiles3.naver.net/MjAxNzExMjBfMjYz/MDAxNTExMTg3MzQ5NzQw.C33rKIytDNzdMZldGRoqlfVqj3lzm2YsdFQpncUrO-Qg.Q9GPdA7_7tHRoKSatJDbYitKdsMJPoE6um5zPnp8Wtsg.JPEG.qazqww/porkcutlet.jpg?type=w2"
    elif url == 'pasta':
        menuurl = "http://postfiles1.naver.net/MjAxNzExMjBfMjIy/MDAxNTExMTg3MzQ4Nzkw.7DZ48tw-MIrF5d1Ln6YyGeDwP8xRD99gQBYfH6U1GOwg.VpWD9VYh_zlRBxDmNkw4qZlH-Kfnkd4HvYJuXdSJttMg.JPEG.qazqww/pasta.jpg?type=w2"
    elif url == 'hamburger steak':
        menuurl = "http://postfiles2.naver.net/MjAxNzExMjFfMjk1/MDAxNTExMjM4ODAzODIz.sohCnWIkb4yoO8hmEjl0A-lixNAUlNHyRDhVOUGc4ewg.b8KsAIjy_cL2hyuWzg4Ck_exAAyZA3-pQs1CgBF4-O4g.JPEG.qazqww/hsteak.jpg?type=w2"
    elif url == 'fried chicken':
        menuurl = "http://postfiles10.naver.net/MjAxNzExMjBfMjA5/MDAxNTExMTg3MzQ2OTY2.oqBoc24xgFV_jEE_QVjfrdBiO6-AX1qOhHPLBqCaTUgg.OctCB_YmkhEa9QzAEOxMqI_SH96GnYn9GhIFzb16xKkg.JPEG.qazqww/chicken.jpg?type=w2"
    elif url == 'chicken cuisine':
        menuurl = "http://postfiles9.naver.net/MjAxNzExMjFfMTUy/MDAxNTExMjM5MDA5ODE1.mrITPc20fSiOSbCBGd4RJd1C7B6JcqJzb8GrcdZ6Emkg.wD1JakLLETNWgGTNtwc6l3Rwu_2iA3ZHK3gbf4jTUXQg.JPEG.qazqww/chickencuisine.jpg?type=w2"
    elif url == 'Pyongyang cold noodles':
        menuurl = "http://postfiles5.naver.net/MjAxNzExMjFfODcg/MDAxNTExMjM4ODA1Nzg2.fp_wEHYXs4ZRL16mOWAkvq5RZNQV7MezT0OwsjOhnL0g.L1ylS9IdwfvSX1cZmIbOBryQfPee6eA4gIz37s0uOUEg.JPEG.qazqww/Pyongyang.jpg?type=w2"
    elif url == 'pizza':
        menuurl = "http://postfiles12.naver.net/MjAxNzExMjFfNjkg/MDAxNTExMjM4ODAzNjAw.NG5nlHvLNl_BIV3uT51seTwlEgjmxXk000ghZkQsOB4g.8qcE4qOnPuC_S3iWRfzQB95437b_ODEGRCAP48KUVcAg.JPEG.qazqww/pizza.jpeg?type=w2"
    elif url == 'jokbal and bossam':
        menuurl = "http://postfiles16.naver.net/MjAxNzExMjBfMTQ5/MDAxNTExMTg3MzQ4MzYw.bpU0-Os7l1rY_QJipVJzaZr0aFJh234kAAJjqEwrIvcg.Kl4lkNgfL7ySpE_X9b9sDv_FdvF2aP6Hy62Btc-pBucg.JPEG.qazqww/jokbo.jpg?type=w2"
    elif url == 'meat':
        menuurl = "http://postfiles13.naver.net/MjAxNzExMjBfMjAg/MDAxNTExMTg3MzQ4NjY5.3-fMT63budFhvDez6YTPhw_iedJH9kGcvuPcM5RSqC8g.2LjN1NjaQLpCuJBEXHH3cTE1tiWaDICOdmNiuhv2E0Ug.JPEG.qazqww/meat.jpg?type=w2"
    elif url == 'buffet':
        menuurl = "http://postfiles13.naver.net/MjAxNzExMjFfMTIx/MDAxNTExMjM5MTYzMTk2.aneaM8HyCbF8FaVQsAsnxnTBXiNxJ-PPHl2LObsnU7Yg.0oUh1kbQZzKo0Ktcy53QM_iUDOghhTluD-Ga_57V5SAg.JPEG.qazqww/buffet.jpg?type=w2"
    elif url == 'shabu-shabu':
        menuurl = "http://postfiles15.naver.net/MjAxNzExMjFfMTA2/MDAxNTExMjM5MDA5OTY2.ZCY7Xwax1k3Cel3Pgsr3z2pBUoULDkGmojELaMcAzw4g.GyZ7ECuOMLoWXQ6gDn0OANf2o0307RG9f-Pr8tCfYC4g.JPEG.qazqww/shabu.jpg?type=w2"
    elif url == 'steak':
        menuurl = "http://postfiles8.naver.net/MjAxNzExMjBfMTE0/MDAxNTExMTg3MzQ5MzIy.NATYtaYaaTnrovin5XhxBCmg5FP8yj5mIA7cvid1Dxcg.6FOKxr4u-Ya3RoA5fC41iTHYAKrp07G5uF3msjaaWy8g.JPEG.qazqww/steak.jpg?type=w2"
    elif url == 'raw dishes(sashimi) / seafood':
        menuurl = "http://postfiles16.naver.net/MjAxNzExMjBfMjEz/MDAxNTExMTg3MzQ3ODcy.4ZhzBf9GpQEkTPbRymyeoeJpoCwnQbPVogzDSSlAIbog.fRyepRxUNHkPhUy1YoLLK-xlEjorAXLO4j3KzHyCOAwg.JPEG.qazqww/hoe.jpg?type=w2"
    elif url == 'family restaurant':
        menuurl = "http://postfiles9.naver.net/MjAxNzExMjFfNCAg/MDAxNTExMjM5MTYzMzgw.ra9xYS5FiK7CBojOwQnAro4MTA7fqeuKsMDaQamGp_Ag.-AOEDlOF5X53XEEIcgD3pQkFBq9aGSC-vVcK61XskDUg.JPEG.qazqww/family.jpg?type=w2"
    else:
        menuurl = "nothing"
    
    return menuurl

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

    """
        if int(connect_apiai.get_apiai(content)) > 20000:
            choicemenu = choice(highhigh)
        elif int(connect_apiai.get_apiai(content)) > 12500:
            choicemenu = choice(high)
        elif int(connect_apiai.get_apiai(content)) > 7000:
            choicemenu = choice(mid)
        elif int(connect_apiai.get_apiai(content)) > 4000:
            choicemenu = choice(lowmid)
        else:
            choicemenu = choice(low)
    """
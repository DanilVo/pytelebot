import telebot
import http.client
import urllib.parse
import requests
from telebot import types
from requests import get
import geonamescache
import json


API_KEY_TELE = "5155568476:AAHC3_vVjKjVwzL-zLXejc6SfVVWV1u4_FE"

API_KEY1_WEATHER = "1353ad9c7af9a94f3f41d52e1c656a22abdba01ba8094ab0cfe3609c7385cc92"
BASE_URL_WEATHER = "http://api.positionstack.com/v1/"

API_KEY_LOCATION = "05fe4fc8294f68ce34f808282d69b31f"
url_location = "https://api.ambeedata.com/weather/latest/by-lat-lng"

bot = telebot.TeleBot(API_KEY_TELE)
# gc = geonamescache.GeonamesCache()
# countries = gc.get_cities_by_name()

mydict = {}

def weather():
    querystring = {"lat": f"{lat}", "lng": f"{lng}"}
    headers = {
        'x-api-key': f'{API_KEY1_WEATHER}',
        'Content-type': "application/json"
    }
    response = requests.request(
        "GET", url_location, headers=headers, params=querystring).json()
    res =  round(((response['data']['apparentTemperature'])-32)*5/9)
    return res

@bot.message_handler(commands=['weather'])
def show_weather(message):
    msg = bot.send_message(message.chat.id, "enter location")
    bot.register_next_step_handler(msg, location_name)


def location_name(message):
    # if message.text.lower() == "yes":
        global lat,lng
        conn = http.client.HTTPConnection('api.positionstack.com')
        params = urllib.parse.urlencode({
            'access_key': f'{API_KEY_LOCATION}',
            'query': f'{message.text}',
            'limit': 1,
            'output': 'json'
        })
        conn.request('GET', f'/v1/forward?{params}')

        res = conn.getresponse().read()
        dec = res.decode()
        ajson = json.loads(dec)
        lat = ajson['data'][0]['latitude']
        lng = ajson['data'][0]['longitude']
        print(lat,lng)
        ls = [lat,lng]
        # mydict[lat] = lng
        bot.send_message(message.chat.id, weather())
        return lat, lng
    # elif message.text.lower() == "no":
    #     bot.send_message(message.chat.id, "good bye")

# def get_location(message):
#     global lat, lng
#     msg = bot.register_next_step_handler(message, weather)
#     conn = http.client.HTTPConnection('api.positionstack.com')
#     params = urllib.parse.urlencode({
#         'access_key': f'{API_KEY_LOCATION}',
#         'query': f'{msg}',
#         'limit': 1,
#         'output':'json'
#         })

#     conn.request('GET', f'/v1/forward?{params}')

#     res = conn.getresponse().read()
#     dec = res.decode()
#     ajson = json.load(dec)
#     lat = ajson['data'][0]['latitude']
#     lng = ajson['data'][0]['longitude']
#     return lat, lng


bot.polling()

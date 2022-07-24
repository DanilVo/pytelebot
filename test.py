import http.client, urllib.parse
import json
import telebot
import requests
from requests import get

API_KEY_TELE = "5155568476:AAHC3_vVjKjVwzL-zLXejc6SfVVWV1u4_FE"

API_KEY1_WEATHER = "1353ad9c7af9a94f3f41d52e1c656a22abdba01ba8094ab0cfe3609c7385cc92"
BASE_URL_WEATHER = "http://api.positionstack.com/v1/"

API_KEY_LOCATION = "05fe4fc8294f68ce34f808282d69b31f"
url_location = "https://api.ambeedata.com/weather/latest/by-lat-lng"


bot = telebot.TeleBot(API_KEY_TELE)

def get_location():
    global lat, lng
    conn = http.client.HTTPConnection('api.positionstack.com')
    params = urllib.parse.urlencode({
        'access_key': f'{API_KEY_LOCATION}',
        'query': 'london',
        'limit': 1,
        'output':'json'
        })

    conn.request('GET', f'/v1/forward?{params}')

    res = conn.getresponse().read()
    lat = res.decode()
    res1 = json.loads(lat)
    # lng = res.decode('utf-8')[43:52]
    print(res1['data'][0]['latitude'])
    print(res1['data'][0]['longitude'])

    # return (lat, lng)

get_location()

def weather(): 
    querystring = {"lat":f"{lat}","lng":f"{lng}"}
    headers = {
        'x-api-key': f'{API_KEY1_WEATHER}',
        'Content-type': "application/json"
        }
    response = requests.request("GET", url_location, headers=headers, params=querystring).json()
    return round(((response['data']['apparentTemperature'])-32)*5/9)

@bot.message_handler(commands=['weather'])
def show_weather(message):
    bot.send_message(message.chat.id, weather())

# bot.polling()




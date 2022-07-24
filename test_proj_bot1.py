import telebot
import http.client
import urllib.parse
import requests
from requests import get
import json

API_KEY_TELE = "5155568476:AAHC3_vVjKjVwzL-zLXejc6SfVVWV1u4_FE"

API_KEY1_WEATHER = "1353ad9c7af9a94f3f41d52e1c656a22abdba01ba8094ab0cfe3609c7385cc92"
BASE_URL_WEATHER = "http://api.positionstack.com/v1/"

API_KEY_LOCATION = "05fe4fc8294f68ce34f808282d69b31f"
url_location = "https://api.ambeedata.com/weather/latest/by-lat-lng"

bot = telebot.TeleBot(API_KEY_TELE)

@bot.message_handler(commands=['start'])
def help_start(message):
    bot.send_message(message.chat.id, 'Welcome to Danils bot!\nEnter /help for commands')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Avilable commands:\n/weather")

@bot.message_handler(commands=['weather'])
def show_weather(message):
    msg = bot.send_message(message.chat.id, "Enter city to see weather conditions:")
    bot.register_next_step_handler(msg, location_name)

def location_name(message):
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
    print((len(ajson["data"])))
    if len(ajson["data"]) > 0:
        lat = ajson['data'][0]['latitude']
        lng = ajson['data'][0]['longitude']
        country_name = ajson['data'][0]['country']
        print(lat,',',lng)
        bot.send_message(message.chat.id, f'Weather in {country_name}, {message.text.capitalize()} {weather()} celcius')
        return lat, lng
    else:
        bot.send_message(message.chat.id, "No such city found!\nTry again /weather")

def weather():
    querystring = {"lat": f"{lat}", "lng": f"{lng}"}
    headers = {
        'x-api-key': f'{API_KEY1_WEATHER}',
        'Content-type': "application/json"
    }
    response = requests.request(
        "GET", url_location, headers=headers, params=querystring).json()
    res = round(((response['data']['apparentTemperature'])-32)*5/9)
    return res

bot.polling()

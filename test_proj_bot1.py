import telebot
import http.client
import urllib.parse
import requests
from requests import get
import json
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()

configure()

bot = telebot.TeleBot(os.getenv('API_KEY_TELE'))

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
        'access_key': f'{os.getenv("API_KEY_LOCATION")}',
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
        bot.send_message(message.chat.id, f'Weather in {country_name}, {message.text.capitalize()} {weather()}')
        return lat, lng
    else:
        bot.send_message(message.chat.id, "No such city found!\nTry again /weather")

def weather():
    querystring = {"lat": f"{lat}", "lng": f"{lng}"}
    headers = {
        'x-api-key': f'{os.getenv("API_KEY1_WEATHER")}',
        'Content-type': "application/json"
    }
    response = requests.request(
        "GET", os.getenv("url_location"), headers=headers, params=querystring).json()
    res = round(((response['data']['apparentTemperature'])-32)*5/9)
    summary = response['data']['summary']
    return f'{res} celcius, {summary}'

bot.polling()

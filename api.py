import requests
import os
from dotenv import load_dotenv
load_dotenv()
weather_api_key = os.getenv('WEATHER_API_KEY')
def get_weather(coord, key):
    url = f'http://api.weatherapi.com/v1/current.json?key={key}&q={coord}&lang=ru&aqi=yes'
    response = requests.get(url)
    data = response.json()

    w = {
        "temp_c": data["current"]["temp_c"],
        "condition_text": data["current"]["condition"]["text"],
        "wind_kph": data["current"]["wind_kph"],
        "gust_kph": data["current"]["gust_kph"],
        "vis_km": data["current"]["vis_km"],
        "humidity": data["current"]["humidity"],
        "cloud": data["current"]["cloud"],
        "co": data["current"]["air_quality"]["co"],
        "o3": data["current"]["air_quality"]["o3"],
        "so2": data["current"]["air_quality"]["so2"],
        "pm2_5": data["current"]["air_quality"]["pm2_5"],
        "pm10": data["current"]["air_quality"]["pm10"],
        "air-q": ""
    }

    avg = (int(w['co']) + int(w['o3']) + int(w['so2']) + int(w['pm2_5']) + int(w['pm10'])) / 5

    if avg < 50: w['air-q'] = 'В норме'
    elif 50 <= avg < 100: w['air-q'] = 'Умеренное загрязнение'
    elif 100 <= avg < 150: w['air-q'] = 'Плохое качество воздуха'
    else: w['air-q'] = 'Очень плохое качество воздуха'

    return w

import json
import requests
import os

def weather_json(w_city, apikey):
    api = f'http://api.openweathermap.org/data/2.5/weather?q={w_city}&appid={apikey}&lang=kr&units=metric'
    response = requests.get(api)
    return response.json()


def pm_json(w_city, apikey):
    location_api = f'http://api.openweathermap.org/geo/1.0/direct?q={w_city}&limit=5&appid={apikey}'
    location_response = requests.get(location_api)
    location_api_result = location_response.json()
    lat = location_api_result[0]['lat']
    lon = location_api_result[0]['lon']

    api = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={apikey}'
    response = requests.get(api)
    return response.json()


def weather(w_city='Seoul'):
    apikey = os.getenv("weather_api")
    weather_api = weather_json(w_city, apikey)
    pm_api = pm_json(w_city, apikey)
    pm2_5 = pm_api['list'][0]['components']['pm2_5']
    pm10 = pm_api['list'][0]['components']['pm10']

    w_cities = [
    {'name': '서울', 'value': 'SEOUL'},
    {'name': '부산', 'value': 'BUSAN'},
    {'name': '대구', 'value': 'DAEGU'},
    {'name': '대전', 'value': 'DAEJEON'},
    {'name': '전주', 'value': 'JEONJU'},
    {'name': '광주', 'value': 'GWANGJU'},
    {'name': '인천', 'value': 'INCHEON'},
    {'name': '제주', 'value': 'JEJU'},
    {'name': '세종', 'value': 'SEJONG'},
    {'name': '춘천', 'value': 'CHUNCHEON'},
    {'name': '강릉', 'value': 'GANGNEUNG'},
    {'name': '해남', 'value': 'HAENAM'},

]

    if pm2_5 > 75:        
        fine_dust = '매우나쁨'
    elif 50 < pm2_5 <= 75:
        fine_dust = '나쁨'
    elif 25 < pm2_5 <= 50:
        fine_dust = '보통'
    elif 10 < pm2_5 <= 25:
        fine_dust = '좋음'
    elif 0 <= pm2_5 <= 10:
        fine_dust = '매우좋음'
    else:
        fine_dust = '확인불가'

    if pm10 > 200:
        ultrafine_dust = '매우나쁨'
    elif 100 < pm10 <= 200:
        ultrafine_dust = '나쁨'
    elif 50 < pm10 <= 100:
        ultrafine_dust = '보통'
    elif 20 < pm10 <= 50:
        ultrafine_dust = '좋음'
    elif 0 <= pm10 <= 20:
        ultrafine_dust = '매우좋음'
    else:
        ultrafine_dust = '확인불가'
    context = {
        'w_city': w_city,
        'weather': weather_api['weather'][0]['description'],
        'temp': round(weather_api['main']['temp'], 1), 
        'feels_like': round(weather_api['main']['feels_like'], 1),
        'temp_min': round(weather_api['main']['temp_min'], 1),
        'temp_max': round(weather_api['main']['temp_max'], 1),
        'humidity': weather_api['main']['humidity'],
        'fine_dust': fine_dust,
        'ultrafine_dust': ultrafine_dust,
        'w_cities': w_cities,
        'icon': f"https://openweathermap.org/img/wn/{weather_api['weather'][0]['icon']}@2x.png",
    }

    return context
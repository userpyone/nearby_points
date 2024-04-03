import requests
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('API_KEY')
def get_air_quality(lat, lon, API_key):
    url = f'http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={str(lat)}&lon={str(lon)}&appid={API_key}'
    response = requests.get(url)
    data = response.json()
    first_item = data['list'][0]
    components = first_item['components']
    components_dict = {
        'co': components['co'],
        'no': components['no'],
        'no2': components['no2'],
        'o3': components['o3'],
        'so2': components['so2'],
        'pm2_5': components['pm2_5'],
        'pm10': components['pm10'],
        'nh3': components['nh3']
    }
    return components_dict

# print(get_air_quality(59.832321, 30.330957, api_key))
# {'co': 240.33, 'no': 0, 'no2': 2.23, 'o3': 80.82, 'so2': 0.61, 'pm2_5': 0.5, 'pm10': 0.56, 'nh3': 0.49}

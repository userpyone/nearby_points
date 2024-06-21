from geopy.geocoders import Nominatim
from geopy.geocoders import ArcGIS
import geocoder
import requests

def get_coordinates_by_address(address):
    # ArcGIS API
    geolocator_arcgis = ArcGIS()
    location = geolocator_arcgis.geocode(address)
    if location != None:
        # return {'lat': round(location.latitude, 6),
        #         'lon': round(location.longitude, 6)}
        return [round(location.latitude, 6), round(location.longitude, 6)]
    else:
        print('Location is None!')
def get_coordinates_by_address_osm(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                return {'lat': round(lat, 6),
                        'lon': round(lon, 6)}
            else:
                print("Адрес не найден.")
        else:
            print("Ошибка при выполнении запроса:", response.status_code)
    except Exception as e:
        print("Ошибка:", e)

# address = 'Санкт-Петербург, Кронверкский проспект, 49'
# print('By Arcgis:', get_coordinates_by_address(address))
# print('By osm:', get_coordinates_by_address_osm(address))
# {'lat': 59.928894, 'lon': 30.406338}
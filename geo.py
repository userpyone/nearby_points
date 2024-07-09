from geopy.geocoders import ArcGIS
import geocoder
import requests
def get_coordinates_by_address(address):
    geolocator_arcgis = ArcGIS()
    location = geolocator_arcgis.geocode(address)
    if location != None:
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

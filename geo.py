from geopy.geocoders import Nominatim
from geopy.geocoders import ArcGIS
import geocoder

address = 'Пулковское шоссе, 14с6, Санкт-Петербург'
def get_coordinates_by_address(address):
    # ArcGIS API
    geolocator_arcgis = ArcGIS()
    location = geolocator_arcgis.geocode(address)
    if location != None:
        return {'lat': round(location.latitude, 6),
                'lon': round(location.longitude, 6)}
    else:
        print('Location is None!')
# print(get_coordinates_by_address(address))
# {'lat': 59.831436, 'lon': 30.330027}
# geolocator_arcgis = ArcGIS()
# location = geolocator_arcgis.geocode(address)
# print(round(location.latitude, 6), round(location.longitude, 6))

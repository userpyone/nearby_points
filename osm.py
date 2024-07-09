import requests
import overpy
import json
import osmnx as ox
import io
import urllib.request
import random

'''OVERPASS API (OSM)'''
def get_point_info(lat, lon):
    url = (f'https://overpass-api.de/api/interpreter?data=[out:json];is_in({str(lat)}, {str(lon)});out meta;')
    response = requests.get(url)
    data = response.json()
    return data
def osm_request(data):
    url = f'https://overpass-api.de/api/interpreter?data={data}'
    response = requests.get(url)
    data = response.json()
    return data

def vk_request(data):
    url = f'https://maps.mail.ru/osm/tools/overpass/api/interpreter?data={data}'
    response = requests.get(url)
    data = response.json()
    return data

def overpy_request(req):
    api = overpy.Overpass()
    result = api.query(req)
    return result

def get_region_district_by_json(data):
    districts = []
    districts_names = []
    districts_ords = []
    districts_ords_names = []
    for element in data['elements']:
        if 'tags' in element:
            tags = element['tags']
            if 'name' in tags and 'admin_level' in tags:
                name = tags['name']
                if 'район' in name.lower():
                    districts.append(name)
                    districts_names.append(name)
                if 'округ' in name.lower():
                    districts.append(name)
                    districts_ords.append(name)
                    districts_ords_names.append(name)
    return districts_names[0].split()[0], districts_ords_names[0]

coord = '55.756628, 37.553022'
radius = '2000'

def get_osm_values(radius, coord):
    shops = f'[out:json];\
    node(around:{radius}, {coord})["shop"="supermarket"];\
    out count;\
    node(around:{radius}, {coord})["shop"="bakery"];\
    out count;\
    node(around:{radius}, {coord})["amenity"="cafe"];\
    out count;\
    way(around:{radius}, {coord})["shop"="mall"];\
    out count;\
    node(around:{radius}, {coord})["shop"="outpost"];\
    out count;\
    node(around:{radius}, {coord})["shop"="electronics"];\
    out count;'

    infrastructure = f'way(around:{radius}, {coord})["amenity"="school"];\
    out count;\
    way(around:{radius}, {coord})["amenity"="kindergarten"];\
    out count;\
    way(around:{radius}, {coord})["amenity"="hospital"];\
    way(around:{radius}, {coord})["amenity"="clinic"];\
    out count;\
    node(around:{radius}, {coord})["amenity"="pharmacy"];\
    out count;\
    node(around:{radius}, {coord})["amenity"="bank"];\
    out count;'

    culture = f'node(around:{radius}, {coord})["amenity"="library"];\
    out count;\
    node(around:{radius}, {coord})["amenity"="cinema"];\
    out count;\
    node(around:{radius}, {coord})["amenity"="theatre"];\
    out count;'

    sport = f'node(around:{radius}, {coord})["leisure"="sports_centre"];\
    out count;\
    node(around:{radius}, {coord})["leisure"="sports_hall"];\
    out count;\
    relation(around:{radius}, {coord})["leisure"="stadium"];\
    out count;\
    way(around:{radius}, {coord})["sport"="swimming"];\
    out count;'

    transport = f'way(around:{radius}, {coord})["highway"="footway"];\
    out count;\
    way(around:{radius}, {coord})["highway"="cycleway"];\
    out count;\
    node(around:{radius}, {coord})["station"="subway"];\
    out count;\
    node(around:{radius}, {coord})["highway"="bus_stop"];\
    out count;\
    way(around:{radius}, {coord})["parking"="surface"];\
    out count;\
    node(around:{radius}, {coord})["parking"="underground"];\
    out count;\
    node(around:{radius}, {coord})["amenity"="bicycle_parking"];\
    out count;'

    ecology = f'way(around:{radius}, {coord})["leisure"="park"];\
    out count;\
    way(around:{radius}, {coord})["natural"="water"];\
    out count;\
    way(around:{radius}, {coord})["natural"="wood"];\
    out count;'
    return osm_request(shops + infrastructure + culture + sport + transport + ecology)
def new_request(radius, coord):
    shops = f'''[out:json];
    (node(around:{radius}, {coord})["shop"="outpost"];);
    out count;
    (node(around:{radius}, {coord})["amenity"="post_office"];
      way(around:{radius}, {coord})["amenity"="post_office"];);
    out count;
    (node(around:{radius}, {coord})["shop"="supermarket"];);
    out count;
    (node(around:{radius}, {coord})["shop"="beverages"];);
    out count;
    (node(around:{radius}, {coord})["shop"="electronics"];);
    out count;
    (node(around:{radius}, {coord})["shop"="clothes"];);
    out count;
    (node(around:{radius}, {coord})["shop"="shoes"];);
    out count;
    (node(around:{radius}, {coord})["shop"="pet"];);
    out count;
    (node(around:{radius}, {coord})["shop"="appliance"];);
    out count;
    (node(around:{radius}, {coord})["shop"="furniture"];);
    out count;
    (node(around:{radius}, {coord})["shop"="dry_cleaning"];);
    out count;
    (node(around:{radius}, {coord})["shop"="hairdresser"];);
    out count;
    (node(around:{radius}, {coord})["shop"="beauty"];);
    out count;
    (way(around:{radius}, {coord})["amenity"="fuel"];);
    out count;
    (node(around:{radius}, {coord})["shop"="car_repair"];
      node(around:{radius}, {coord})["amenity"="car_repair"];);
    out count;'''

    fun = f'''(node(around:{radius}, {coord})["amenity"="cafe"];);
    out count;
    (node(around:{radius}, {coord})["amenity"="restaurant"];);
    out count;
    (node(around:{radius}, {coord})["shop"="bakery"];);
    out count;
    (node(around:{radius}, {coord})["shop"="confectionery"];);
    out count;
    (node(around:{radius}, {coord})["amenity"="bar"];);
    out count;
    (node(around:{radius}, {coord})["amenity"="pub"];);
    out count;
    (node(around:{radius}, {coord})["amenity"="nightclub"];);
    out count;
    (way(around:{radius}, {coord})["shop"="mall"];);
    out count;
    (node(around:{radius}, {coord})["amenity"="cinema"];);
    out count;'''

    edu = f'''(node(around:{radius}, {coord})["amenity"="school"];
      way(around:{radius}, {coord})["amenity"="school"];);
    out count;
    (node(around:{radius}, {coord})["amenity"="kindergarten"];);
    out count;
    (node(around:{radius}, {coord})["amenity"="university"];
    relation(around:{radius}, {coord})["amenity"="university"];);
    out count;
    (node(around:{radius}, {coord})["amenity"="library"];
      way(around:{radius}, {coord})["amenity"="library"];);
    out count;'''

    health = f'''(
      node(around:{radius}, {coord})["amenity"="hospital"];
      way(around:{radius}, {coord})["amenity"="hospital"];);
    out count;
    (node(around:{radius}, {coord})["amenity"="clinic"];);
    out count;
    (node(around:{radius}, {coord})["amenity"="pharmacy"];
      way(around:{radius}, {coord})["amenity"="pharmacy"];);
    out count;
    (node(around:{radius}, 59.956940, 30.318312)["healthcare"="dentist"];
    relation(around:{radius}, 59.956940, 30.318312)["healthcare"="dentist"];);
    out count;
    (node(around:{radius}, {coord})["amenity"="veterinary"];
      way(around:{radius}, {coord})["amenity"="veterinary"];);
    out count;
    (node(around:{radius}, {coord})["building"="warehouse"];
      way(around:{radius}, {coord})["building"="warehouse"];);
    out count;'''

    town = f'''
        (node(around:{radius}, {coord})["amenity"="police"];
      way(around:{radius}, {coord})["amenity"="police"];);
    out count;    
    (node(around:{radius}, {coord})["amenity"="fire_station"];
      way(around:{radius}, {coord})["amenity"="fire_station"];
      relation(around:{radius}, {coord})["amenity"="fire_station"];);
    out count;    
    (node(around:{radius}, {coord})["office"="government"];
      way(around:{radius}, {coord})["office"="government"];);
    out count;'''

    return osm_request(shops + fun + edu + health + town)

'''1 shops + fun + edu + health + town'''
'''2 transport + sport + nature + tech'''
'shops + fun + edu + health + sport + transport + nature + town + tech'

def new_request2(radius, coord):
    transport = f'''[out:json];
            (node(around:{radius}, {coord})["railway"="subway_entrance"];);
        out count;
        (node(around:{radius}, {coord})["highway"="bus_stop"];);
        out count;
        (node(around:{radius}, {coord})["amenity"="parking"];
          relation(around:{radius}, {coord})["amenity"="parking"];);
        out count;
        (node(around:{radius}, {coord})["parking"="underground"];
          way(around:{radius}, {coord})["parking"="underground"];);
        out count;
        (node(around:{radius}, {coord})["railway"="station"];
          way(around:{radius}, {coord})["railway"="station"];);
        out count;
        (node(around:{radius}, {coord})["amenity"="bicycle_parking"];
          way(around:{radius}, {coord})["amenity"="bicycle_parking"];
          relation(around:{radius}, {coord})["amenity"="bicycle_parking"];);
        out count;
        (way(around:{radius}, {coord})["highway"="cycleway"];);
        out count;
        (node(around:{radius}, {coord})["amenity"="car_rental"];
          relation(around:{radius}, {coord})["amenity"="car_rental"];);
        out count;'''

    sport = f'''(
          node(around:{radius}, {coord})["leisure"="sports_centre"];);
        out count;

        (node(around:{radius}, {coord})["leisure"="fitness_centre"];);
        out count;

        (node(around:{radius}, {coord})["leisure"="pitch"];
          way(around:{radius}, {coord})["leisure"="pitch"];
          relation(around:{radius}, {coord})["leisure"="pitch"];);
        out count;

        (node(around:{radius}, {coord})["shop"="sports"];
          way(around:{radius}, {coord})["shop"="sports"];
          relation(around:{radius}, {coord})["shop"="sports"];);
        out count;'''

    nature = f'''(way(around:{radius}, {coord})["leisure"="park"];
          relation(around:{radius}, {coord})["leisure"="park"];);
        out count;
        (way(around:{radius}, {coord})["natural"="water"];
          relation(around:{radius}, {coord})["natural"="water"];);
        out count;
        (way(around:{radius}, {coord})["waterway"="river"];
          relation(around:{radius}, {coord})["waterway"="river"];);
        out count;
        (way(around:{radius}, {coord})["natural"="wood"];
          relation(around:{radius}, {coord})["natural"="wood"];);
        out count;
        (node(around:{radius}, {coord})["natural"="beach"];
          relation(around:{radius}, {coord})["natural"="beach"];);
        out count;'''

    tech = f'''(node(around:{radius}, {coord})["building"="commercial"];
          relation(around:{radius}, {coord})["building"="commercial"];
          node(around:{radius}, {coord})["building"="office"];
          relation(around:{radius}, {coord})["building"="office"];);
        out count;
        (node(around:{radius}, {coord})["office"="company"];
          relation(around:{radius}, {coord})["office"="company"];);
        out count;    
        (node(around:{radius}, {coord})["building"="industrial"];
          relation(around:{radius}, {coord})["building"="industrial"];);
        out count;    
        (node(around:{radius}, {coord})["landuse"="industrial"];
          way(around:{radius}, {coord})["landuse"="industrial"];
          relation(around:{radius}, {coord})["landuse"="industrial"];);
        out count;'''

    return osm_request(transport + sport + nature + tech)


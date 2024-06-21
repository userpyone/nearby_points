import requests
import matplotlib.pyplot as plt
import overpy
import geopandas as gpd
import pandas as pd
import numpy as np
import json
import h3
import folium
import osmnx as ox
from shapely import wkt
from folium.plugins import HeatMap
from shapely.geometry import Polygon
from shapely.geometry import Point
import io
import urllib.request
import random
from cairo import ImageSurface, FORMAT_ARGB32, Context
import mercantile
from format import sort_by_admin_level
from format import get_totals

'''OVERPASS API (OSM)'''
def get_point_info(lat, lon):
    url = (f'https://overpass-api.de/api/interpreter?data=[out:json];is_in({str(lat)}, {str(lon)});out meta;')
    response = requests.get(url)
    # print(url)
    data = response.json()
    return data
# print(sort_by_admin_level(get_point_info(55.759413, 37.597753)))
# print(get_point_info(55.759413, 37.597753))
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

# district, region = get_region_district_by_json(get_point_info(55.759413, 37.597753))
# print(district)
# print(region)


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

# r1 = get_osm_values(radius, coord)
# res = get_totals(r1)
# print(res)
# res = get_totals(get_osm_values(1000, str(coord)))
# print(res)

# print(sort_by_admin_level(osm_request('[out:json];is_in(59.832321, 30.330957);out;')))


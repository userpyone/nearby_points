from math import radians, cos, sin, asin
import json
def load_metro_points_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    metro_points = {}
    for line in data["lines"]:
        for station in line["stations"]:
            name = station["name"]
            lat = station["lat"]
            lng = station["lng"]
            metro_points[name] = (lat, lng)
    return metro_points
def distance_haversine(point_1: tuple, point_2: tuple):
    d_earth = 2.0 * 6372.8
    lat1, long1 = tuple(radians(c) for c in point_1)
    lat2, long2 = tuple(radians(c) for c in point_2)
    d = sin((lat2 - lat1) / 2.0) ** 2.0 + cos(lat1) * cos(lat2) * sin(
        (long2 - long1) / 2.0) ** 2.0
    return d_earth * asin(d ** 0.5)
def find_nearest(point_1: tuple, points: dict):
    dists = {p: distance_haversine(point_1, points[p]) for p in points}
    name, dist = min(dists.items(), key=lambda d: d[1])
    result = {'name': name, 'distance': dist,
            'dist_coef': 3 if dist <= 1.0 else 2 if dist < 2.0 else 1}
    return result['name']

# Test
# point_1 = (59.831721, 30.327388)
# metro_points = load_metro_points_from_json('spb_subway_stations.json')
# print(find_nearest(point_1, metro_points))

# Input Dict Example
# metro_points = {
#     'Новокосино': (55.745113, 37.864052),
#     'Перово': (55.75098, 37.78422),
#     'Ховрино': (55.8777, 37.4877),
#     }
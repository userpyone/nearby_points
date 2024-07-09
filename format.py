import json
from geo import get_coordinates_by_address
from osm import osm_request
def sort_by_admin_level(data):
    area_data_dict = {}
    for element in data['elements']:
        if element['type'] == 'area' and 'tags' in element:
            tags = element['tags']
            name = tags.get('name', None)
            admin_level = tags.get('admin_level', None)
            if name is not None:
                if admin_level is not None:
                    key = admin_level
                else:
                    key = name
                area_data_dict[key] = name
    numeric_keys = [key for key in area_data_dict.keys() if str(key).isdigit()]
    sorted_numeric_keys = sorted(numeric_keys, key=lambda x: int(x))
    sorted_dict = {key: area_data_dict[key] for key in sorted_numeric_keys}
    last_two_keys = list(sorted_dict.keys())[-2:]
    last_two_values = [sorted_dict[key] for key in last_two_keys]
    return last_two_values
def text_by_name_tag(data):
    names = []
    if 'elements' in data:
        elements = data['elements']
        for element in elements:
            if 'tags' in element and 'name' in element['tags']:
                name_value = element['tags']['name']
                names.append(name_value)

    return names
def get_totals(data):
    t = []
    if 'elements' in data and isinstance(data['elements'], list):
        elements = data['elements']
        for i in range(len(elements)):
            element = elements[i]
            if 'tags' in element and isinstance(element['tags'], dict):
                if 'total' in element['tags']:
                    total_value = element['tags']['total']
                    t.append(total_value)
    return t
def get_number_by_district(district_name, json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        if item["district"] == district_name:
            return item["number"]
def is_city(user_input):
    file_path = 'data/russian-cities.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        cities = json.load(file)
    city_names = [city['name'].replace('ё', 'е').lower() for city in cities]
    user_input_lower = user_input.lower().replace('ё', 'е')
    return any(city.lower() in user_input_lower for city in city_names)
def content1(adr):
    coord = get_coordinates_by_address(adr)
    if coord is not None:
        format_coodr = f'{coord[0]}, {coord[1]}'
        return sort_by_admin_level(osm_request(f'[out:json];is_in({format_coodr});out;')), format_coodr
    else:
        return None, None

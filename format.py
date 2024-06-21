import json
# from osm import get_point_info
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
    # Сортировка
    numeric_keys = [key for key in area_data_dict.keys() if str(key).isdigit()]
    sorted_numeric_keys = sorted(numeric_keys, key=lambda x: int(x))
    sorted_dict = {key: area_data_dict[key] for key in sorted_numeric_keys}
    last_two_keys = list(sorted_dict.keys())[-2:]
    last_two_values = [sorted_dict[key] for key in last_two_keys]
    return last_two_values

# r = get_point_info(59.885566, 30.320093)
# print(sort_by_admin_level('test11.json'))
# {'2': 'Россия',
# '3': 'Северо-Западный федеральный округ',
# '4': 'Санкт-Петербург',
# '5': 'Московский район',
# '8': 'округ Звёздное'}

def text_by_name_tag(data):
    names = []
    # with open(json_file_path, 'r', encoding='utf-8') as file:
    #     data = json.load(file)
    if 'elements' in data:
        elements = data['elements']
        for element in elements:
            if 'tags' in element and 'name' in element['tags']:
                name_value = element['tags']['name']
                names.append(name_value)

    return names

def get_totals(data):
    categories = [
        "Супермаркеты",
        "Пекарни",
        "Кафе",
        "Торговые центры",
        "Пункты выдачи",
        "Магазины техники", #6
        "Школы",
        "Детские сады",
        "Больницы", #9
        "Аптеки",
        "Банки",
        "Библиотеки",
        "Кинотеатры",
        "Театры",
        "Спортивные центры",
        "Спортивные залы",
        "Стадионы",
        "Бассейны", #18
        "Пешеходные дороги",
        "Велосипедные дорожки",
        "Станции метро",
        "Автобусные остановки",
        "Парковки",
        "Подземные парковки",
        "Велосипедные парковки",
        "Парки",
        "Водоемы",
        "Массивы деревьев"
    ]
    t = []
    # totals_dict = {category: None for category in categories}
    if 'elements' in data and isinstance(data['elements'], list):
        elements = data['elements']
        for i in range(min(len(categories), len(elements))):
            element = elements[i]
            if 'tags' in element and isinstance(element['tags'], dict):
                if 'total' in element['tags']:
                    total_value = element['tags']['total']
                    t.append(total_value)
                    # category = categories[i]
                    # totals_dict[category] = total_value

    return t

def get_number_by_district(district_name, json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        if item["district"] == district_name:
            return item["number"]

# print(get_number_by_district('Пресненский', 'data/districts/msk_districts.json'))

def is_city(user_input):
    file_path = 'data/russian-cities.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        cities = json.load(file)
    city_names = [city['name'].replace('ё', 'е').lower() for city in cities]
    user_input_lower = user_input.lower().replace('ё', 'е')
    return any(city.lower() in user_input_lower for city in city_names)

# print(is_city('Орел'))
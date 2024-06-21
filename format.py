import json
from osm import get_point_info
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
    return sorted_dict

print(sort_by_admin_level(get_point_info(60.039141, 30.329985)))
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
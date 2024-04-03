import urllib.request
import json
import fake_headers
from fake_headers import Headers
from fake_useragent import UserAgent
# useragent = UserAgent()
# import json
# filename = 'spb_subway_stations.json'
# with open(filename, 'r', encoding='utf-8') as f:
#     data = json.load(f)
# metro_points = {}
# for line in data["lines"]:
#     for station in line["stations"]:
#         name = station["name"]
#         lat = station["lat"]
#         lng = station["lng"]
#         metro_points[name] = (lat, lng)
# print(metro_points)

# lat_home = float(59.877365)
# long_home = float(30.441556)
#
# coordinates_metro = get_coordinates_from_name('Девяткино', load_metro_points_from_json('spb_subway_stations.json'))
# lat_metro = coordinates_metro[0]
# long_metro = coordinates_metro[1]
#
# link = f'https://yandex.ru/maps/2/saint-petersburg/?ll=30.376538%2C59.869593&mode=routes&rtext={str(lat_home)}%2C{str(long_home)}~{str(lat_metro)}%2C{str(long_metro)}&rtt=mt'
# print(link)

# coord = {'lat': 59.831436, 'lon': 30.330027}
# print(coord['lon'])
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

url = 'https://i5.photo.2gis.com/images/geo/0/30258560110064734_72f9.jpg'
# urllib.request.urlretrieve(url, 'png.png')

# req = urllib.request.Request(url, headers=hdr)
# try:
#     with urllib.request.urlopen(req) as response, open('image.png', 'wb') as out_file:
#         data = response.read()
#         out_file.write(data)
#     print("Изображение успешно загружено.")
# except urllib.error.HTTPError as e:
#     print("Не удалось загрузить изображение. Код ошибки:", e.code)

# print(fake_headers.random_browser())
# print(useragent.random)

# def get_number_by_district(district):
#     with open('data/districts/spb_districts.json', encoding='utf-8') as json_file:
#         data = json.load(json_file)
#     for item in data:
#         if item["district"] == district:
#             return item["number"]
# district = "Адмиралтейский"
# number = get_number_by_district(district)
# print(number)

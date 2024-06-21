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

# from itertools import *
# def check(x):
#        if all(f'3{i}' not in x and f'{i}3' not in x for i in '5678'):
#               return True
# c = 0
# for i in product('012345678', repeat=5):
#        num = ''.join(i)
#        if num[0] != '0':
#               if num.count('3') == 1 and check(num):
#                      c += 1
# print(c)

# from flask import Flask, render_template
#
# app = Flask(__name__)
#
# @app.route('/')
# def home():
#     return render_template('waiting.html')
#
# if __name__ == '__main__':
#     app.run(debug=True)

# import secrets
# secret_key = secrets.token_hex(16)
# print(secret_key)  # Выводит сгенерированный секретный ключ



# from flask import Flask, render_template, request, redirect, url_for, session
# from flask_session import Session
# import os
# from parse import extract_image_urls
#
# app = Flask(__name__)
# app.secret_key = os.getenv('FLASK_KEY')
# app.config['UPLOAD_FOLDER'] = 'static/uploads'
# app.config['SESSION_TYPE'] = 'filesystem'
#
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#
# @app.route('/')
# def index():
#     error = session.pop('error', None)
#     return render_template('main.html', error=error)
#
# @app.route('/process_form', methods=['POST'])
# def process_form():
#     if request.method == 'POST':
#         user_input = request.form['user_input']
#         if user_input.strip() == "" or "kvartiry" not in user_input:
#             session['error'] = "Введите корректную ссылку на объявление"
#             return redirect(url_for('index'))
#
#         user_id = str(uuid.uuid4())
#         session['user_id'] = user_id
#         user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
#         os.makedirs(user_folder, exist_ok=True)
#
#         return render_template('waiting.html')
#
# if __name__ == '__main__':
#     app.run(debug=True)

# totals = get_totals(get_osm_values(1000, format_coodr))
# print(totals)
from geo import get_coordinates_by_address
from format import sort_by_admin_level, get_totals
from osm import osm_request, get_osm_values
def content1(adr):
     coord = get_coordinates_by_address(adr)
     format_coodr = f'{coord[0]}, {coord[1]}'
     return sort_by_admin_level(osm_request(f'[out:json];is_in({format_coodr});out;')), format_coodr
# content, coord = content1('улица Анны Северьяновой, 1/14, Москва')
# print(content)
# res = get_totals(get_osm_values(1000, str(coord)))
# print(res)

from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from format import is_city
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
@app.route('/')
def index():
    error = session.pop('error', None)
    return render_template('main.html', error=error)

@app.route('/process_form', methods=['POST'])
def process_form():
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input.strip() == "":
            session['error'] = "Введите корректный адрес"
            return redirect(url_for('index'))
        if is_city(user_input):
            content, coord = content1(user_input)
            res = get_totals(get_osm_values(1000, str(coord)))
            return render_template('res.html',
                                   address=user_input,
                                   data1=content[0],
                                   data2=content[1],
                                   v1=res[0],
                                   v2=res[1],
                                   v3=res[2],
                                   v4=res[3],
                                   v5=res[4],
                                   v6=res[5],
                                   v7=res[6],
                                   v8=res[7],
                                   v9=res[8],
                                   v10=res[9],
                                   v11=res[10],
                                   v12=res[11],
                                   v13=res[12],
                                   v14=res[13],
                                   v15=res[14],
                                   v16=res[15],
                                   v17=res[16],
                                   v18=res[17],
                                   v19=res[18],
                                   v20=res[19],
                                   v21=res[20],
                                   v22=res[21],
                                   v23=res[22],
                                   v24=res[23],
                                   v25=res[24],
                                   v26=res[25],
                                   v27=res[26],
                                   v28=res[27])
        else:
            session['error'] = "Адрес не содержит название города"
            return redirect(url_for('index'))

@app.route('/redirect')
def redirect_to_main():
    return redirect(url_for('index'))

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('404.html'), 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)

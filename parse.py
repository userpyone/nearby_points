import sys, os
import requests
import time
import traceback
import pickle
import urllib.request
from bs4 import BeautifulSoup
from fake_headers import Headers
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from metro import (load_metro_points_from_json,
                   distance_haversine,
                   find_nearest,
                   get_coordinates_from_station_name)
from geo import get_coordinates_by_address

avito_link = 'https://www.avito.ru/sankt-peterburg/kvartiry/kvartira-studiya_45m_1624et._3678667511'

header = Headers()
# hdr = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'}
useragent = UserAgent()
options = webdriver.ChromeOptions()
# options.add_argument(f'user-agent={useragent.random}')
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(
    executable_path=r'chromedriver\chromedriver.exe',
    options=options)

def get_ways_to_move(driver):
    try:
        elements = driver.find_elements_by_css_selector(".route-snippet-view[role='listitem'][aria-label]")
        result = []
        for element in elements:
            aria_label_value = element.get_attribute("aria-label").replace("\xa0", " ")
            result.append(aria_label_value)
    except Exception as e:
        print(e)
    dict_of_ways = {}
    for i in result:
        dict_of_ways[i.split(', ')[0]] = i.split(', ')[1]
    return dict_of_ways

def get_avito_address(driver, avito_link):
    try:
        '''Адрес и стоимость с авито'''
        driver.get(url=avito_link)
        time.sleep(1)
        #Адрес дома
        address = driver.find_element(By.CLASS_NAME, 'style-item-address__string-wt61A').text
        return address
    except Exception as e:
        print('Ошибка при получении адреса с авито!', e)

def get_avito_price(driver, avito_link):
    try:
        '''Адрес и стоимость с авито'''
        driver.get(url=avito_link)
        time.sleep(1)
        #Стоимость квартиры
        finding_price = driver.find_elements(By.XPATH, "//span[@data-marker='item-view/item-price']")
        price = finding_price[1].text.split(' ')[0] + finding_price[1].text.split(' ')[1]
        return price
    except Exception as e:
        print('Ошибка при получении цены с авито!', e)

def get_nearest_metro(home_coordinates):
    try:
        lon_home = home_coordinates['lon']
        msk_longitude_points = [37.309285, 37.898638]
        spb_longitude_points = [30.229404, 30.554705]
        if spb_longitude_points[0] <= lon_home <= spb_longitude_points[1]:
            metro_stations = load_metro_points_from_json('data/subway_stations/spb_subway_stations.json')
        elif msk_longitude_points[0] <= lon_home <= msk_longitude_points[1]:
            metro_stations = load_metro_points_from_json('data/subway_stations/msk_subway_stations.json')
        else:
            print('Неверный город!')
        nearest_station = find_nearest((home_coordinates['lat'], home_coordinates['lon']),
                                       metro_stations)
        return nearest_station, get_metro_coordinates(nearest_station, metro_stations)
    except Exception as e:
        print('Ошибка при получении ближайшего метро!', e)
        exception_traceback = traceback.format_exc()
        print(exception_traceback)

def get_metro_coordinates(nearest_station, metro_stations):
    try:
        coordinates_metro = get_coordinates_from_station_name(str(nearest_station), metro_stations)
        return coordinates_metro
    except Exception as e:
        print('Ошибка при получении координат метро!', e)

def get_time_from_point_to_point(driver, lat_from, lon_from, lat_to, lon_to):
    try:
        point_to_point_link = (f'https://yandex.ru/maps/2/saint-petersburg/'
                              f'?ll=30.376538%2C59.869593&mode=routes&'
                              f'rtext={str(lat_from)}%2C{str(lon_from)}~'
                              f'{str(lat_to)}%2C{str(lon_to)}&rtt=comparison')

        driver.get(point_to_point_link)
        '''Время от точки до точки'''
        ways = get_ways_to_move(driver)
        # pedestrian_time = ways['Пешком']
        # auto_time = ways['На автомобиле']
        # metro_time = ways['На общественном транспорте']
        # bicycle_time = ways['На велосипеде']
        # scooter_time = ways['На самокате']
        return ways
    except Exception as e:
        print('Ошибка при получении времени от дома до метро!', e)

def get_home_photo(address, headers):
    link = 'https://2gis.ru/'
    driver.get(link)
    input_address = WebDriverWait(driver, 10) \
        .until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div[2]/form/div/input')))
    input_address.send_keys(address)
    input_address.send_keys(Keys.ENTER)
    time.sleep(1)
    click_on_photo = driver.find_element(By.CLASS_NAME, "_1dk5lq4")
    click_on_photo.click()
    try:
        time.sleep(2)
        url = driver.find_element(By.XPATH, '//*[@id="photoViewer"]/div/div/div[2]/div[1]/div[1]/div/img').get_attribute('src')
        print(url)
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as response, open('data/images/image.png', 'wb') as out_file:
                data = response.read()
                out_file.write(data)
            print("Изображение успешно загружено.")
        except urllib.error.HTTPError as e:
            print("Не удалось загрузить изображение. Код ошибки:", e.code)
    except NoSuchElementException:
        print('На странице нет фото')

'''РЕЗУЛЬТАТЫ'''
try:
    home_address = get_avito_address(driver, avito_link)
    home_price = get_avito_price(driver, avito_link)
    print(f'Адрес дома: {home_address}')
    print(f'Стоимость квартиры: {home_price}')
    home_coordinates = get_coordinates_by_address(home_address)
    lat_home = home_coordinates['lat']
    lon_home = home_coordinates['lon']
    print('Координаты квартиры:', home_coordinates)
    nearest_metro, metro_coordinates = get_nearest_metro(home_coordinates)
    lat_metro = metro_coordinates[0]
    lon_metro = metro_coordinates[1]
    print(f'Ближайшее метро: {nearest_metro}')
    print(f'Координаты метро: {metro_coordinates}')
    ways_from_home_to_metro_dict = get_time_from_point_to_point(driver,
                                                               lat_home,
                                                               lon_home,
                                                               lat_metro,
                                                               lon_metro)
    print('Время до метро:', ways_from_home_to_metro_dict)
    '''Фото дома'''
    get_home_photo(home_address, header.generate())
except Exception as e:
    exception_traceback = traceback.format_exc()
    print(exception_traceback)

driver.close()
driver.quit()

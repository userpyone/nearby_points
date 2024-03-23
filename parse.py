import sys, os
import requests
import time
import traceback
import pickle
from bs4 import BeautifulSoup
from fake_headers import Headers
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from metro import (load_metro_points_from_json,
                   distance_haversine,
                   find_nearest,
                   get_coordinates_from_name)

avito_link = 'https://www.avito.ru/sankt-peterburg/kvartiry/apartamenty-studiya_24m_718et._3513735552'
start_address = 'Москва, улица Шумилова, 24А'

useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={useragent.random}')
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(
    executable_path=r'C:\Users\ES\PycharmProjects\rent_bot\chromedriver\chromedriver.exe',
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

def get_coordinates_from_address(driver, address):
    try:
        '''Получение координат по адресу'''
        driver.get(url='https://yandex.ru/maps/geo/rossiya/53000001/')

        # Загрузка cookies
        for cookie in pickle.load(open('cookies.pkl', 'rb')):
            driver.add_cookie(cookie)

        # Закрытие баннера (в темной теме)
        try:
            close_ad = driver.find_element(By.XPATH, "//a[@class='s3110cd67']")
            close_ad.click()
        except Exception:
            print('Баннер не закрыт')

        # Ввод адреса в поиск
        input_address = WebDriverWait(driver, 10) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//input[@class='input__control _bold']")))
        input_address.send_keys(address)

        # input_address.send_keys(Keys.ENTER)
        time.sleep(1)
        # elem_first_list = WebDriverWait(driver, 10) \
        #     .until(EC.presence_of_element_located(
        #     (By.XPATH, "//div[@class='search-snippet-view__body _type_toponym']")))
        elem_first_list = driver.find_element(By.CLASS_NAME, "suggest-item-view")
        elem_first_list.click()

        # Поиск координат на сайте
        try:
            finding_coordinates = WebDriverWait(driver, 5) \
                .until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='toponym-card-title-view__coords-badge']")))
            coordinates = finding_coordinates.text
            lat_home = float(coordinates.split(', ')[0]) # широта
            long_home = float(coordinates.split(', ')[1]) # долгота
            result_coordinates = (lat_home, long_home)
            return result_coordinates
        except Exception as e:
            print('На странице нет координат!', e)
    except Exception as e:
        print('Ошибка при получении координат!', e)

def get_nearest_metro(result_coordinates):
    try:
        long_home = result_coordinates[1]
        msk_longitude_points = [37.309285, 37.898638]
        spb_longitude_points = [30.229404, 30.554705]
        if spb_longitude_points[0] <= long_home <= spb_longitude_points[1]:
            metro_stations = load_metro_points_from_json('spb_subway_stations.json')
        elif msk_longitude_points[0] <= long_home <= msk_longitude_points[1]:
            metro_stations = load_metro_points_from_json('msk_subway_stations.json')
        else:
            print('Неверный город!')
        nearest_station = find_nearest(result_coordinates, metro_stations)
        return nearest_station, get_metro_coordinates(nearest_station, metro_stations)
    except Exception as e:
        print('Ошибка при получении ближайшего метро!', e)

def get_metro_coordinates(nearest_station, metro_stations):
    try:
        coordinates_metro = get_coordinates_from_name(str(nearest_station), metro_stations)
        # lat_metro = coordinates_metro[0]
        # long_metro = coordinates_metro[1]
        return coordinates_metro
    except Exception as e:
        print('Ошибка при получении координат метро!', e)


def get_time_from_home_to_metro(driver, lat_home, long_home, lat_metro, long_metro):
    try:
        home_to_metro_link = (f'https://yandex.ru/maps/2/saint-petersburg/'
                              f'?ll=30.376538%2C59.869593&mode=routes&'
                              f'rtext={str(lat_home)}%2C{str(long_home)}~'
                              f'{str(lat_metro)}%2C{str(long_metro)}&rtt=comparison')

        driver.get(home_to_metro_link)
        '''Время от дома до метро'''
        ways = get_ways_to_move(driver)
        # pedestrian_time = ways['Пешком']
        # auto_time = ways['На автомобиле']
        # metro_time = ways['На общественном транспорте']
        # bicycle_time = ways['На велосипеде']
        # scooter_time = ways['На самокате']
        return ways
    except Exception as e:
        print('Ошибка при получении времени от дома до метро!', e)

'''РЕЗУЛЬТАТЫ'''

home_address = get_avito_address(driver, avito_link)
home_price = get_avito_price(driver, avito_link)
print(f'Адрес дома: {home_address}')
print(f'Стоимость квартиры: {home_price}')
home_coordinates = get_coordinates_from_address(driver, home_address)
lat_home = home_coordinates[0]
long_home = home_coordinates[1]
print('Координаты квартиры:', home_coordinates)
nearest_metro, metro_coordinates = get_nearest_metro(home_coordinates)
lat_metro = metro_coordinates[0]
long_metro = metro_coordinates[1]
print(f'Ближайшее метро: {nearest_metro}')
print(f'Координаты метро: {metro_coordinates}')
ways_from_home_to_metro_dict = get_time_from_home_to_metro(driver,
                                                           lat_home,
                                                           long_home,
                                                           lat_metro,
                                                           long_metro)
print(ways_from_home_to_metro_dict)

driver.close()
driver.quit()

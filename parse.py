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
# address_str = 'Санкт-Петербург, Пулковское ш., 14'

def get_ways_to_move(driver):
    try:
        elements = driver.find_elements_by_css_selector(".route-snippet-view[role='listitem'][aria-label]")
        result = []
        for element in elements:
            aria_label_value = element.get_attribute("aria-label").replace("\xa0", " ")
            result.append(aria_label_value)
    except Exception as e:
        pass
        print(e)
    dict_of_ways = {}
    for i in result:
        dict_of_ways[i.split(', ')[0]] = i.split(', ')[1]
    return dict_of_ways

useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={useragent.random}')
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(
    executable_path=r'C:\Users\ES\PycharmProjects\rent_bot\chromedriver\chromedriver.exe',
    options=options)
try:
    '''Адрес и стоимость с авито'''
    driver.get(url=avito_link)
    time.sleep(1)
    #Адрес дома
    address = driver.find_element(By.CLASS_NAME, 'style-item-address__string-wt61A').text
    #Стоимость квартиры
    finding_price = driver.find_elements(By.XPATH, "//span[@data-marker='item-view/item-price']")
    price = finding_price[1].text.split(' ')[0] + finding_price[1].text.split(' ')[1]
    print('Адрес: ', address)
    print('Стоимость: ', price)

    useragent = UserAgent()
    '''Получение координат по адресу'''
    driver.get(url='https://yandex.ru/maps/geo/rossiya/53000001/')
    # Загрузка cookies
    for cookie in pickle.load(open('cookies.pkl', 'rb')):
        driver.add_cookie(cookie)

    # Закрытие баннера (в темной теме)
    try:
        close_ad = driver.find_element(By.XPATH, "//a[@class='s3110cd67']")
        close_ad.click()
    except Exception as e:
        print(e)

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
        print('Координаты: ', lat_home, long_home)
    except Exception as e:
        print(e)
        print('На странице нет координат!')

    '''Получение ближайшего метро'''
    try:
        msk_longitude_points = [37.309285, 37.898638]
        spb_longitude_points = [30.229404, 30.554705]
        if spb_longitude_points[0] <= long_home <= spb_longitude_points[1]:
            metro_stations = load_metro_points_from_json('spb_subway_stations.json')
        elif msk_longitude_points[0] <= long_home <= msk_longitude_points[1]:
            metro_stations = load_metro_points_from_json('msk_subway_stations.json')
        else:
            print('Неверный город!')
        nearest_station = find_nearest(result_coordinates, metro_stations)
        print('Ближайшее метро: ', nearest_station)

        '''Получение координат метро'''
        coordinates_metro = get_coordinates_from_name(str(nearest_station), metro_stations)
        lat_metro = coordinates_metro[0]
        long_metro = coordinates_metro[1]
        home_to_metro_link = (f'https://yandex.ru/maps/2/saint-petersburg/'
                              f'?ll=30.376538%2C59.869593&mode=routes&'
                              f'rtext={str(lat_home)}%2C{str(long_home)}~'
                              f'{str(lat_metro)}%2C{str(long_metro)}&rtt=comparison')

        driver.get(home_to_metro_link)
        '''Время от дома до метро'''
        ways = get_ways_to_move(driver)
        pedestrian_time = ways['Пешком']
        auto_time = ways['На автомобиле']
        metro_time = ways['На общественном транспорте']
        bicycle_time = ways['На велосипеде']
        scooter_time = ways['На самокате']
        print(pedestrian_time)

        time.sleep(1)

    except Exception as e:
        traceback.print_exc()

except Exception as e:
    print(e)
finally:
    driver.close()
    driver.quit()

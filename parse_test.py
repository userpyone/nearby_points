import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent
import fake_headers
from fake_headers import Headers
useragent = UserAgent()
options = webdriver.ChromeOptions()
# options.add_argument(f'user-agent={useragent.random}')
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
        pass
        print(e)
    dict_of_ways = {}
    for i in result:
        dict_of_ways[i.split(', ')[0]] = i.split(', ')[1]
    return dict_of_ways

def get_ways_by_any_points(lat_start, long_start, lat_end, long_end, driver):
    url = (f'https://yandex.ru/maps/2/saint-petersburg/'
                              f'?ll=30.376538%2C59.869593&mode=routes&'
                              f'rtext={str(lat_start)}%2C{str(long_start)}~'
                              f'{str(lat_end)}%2C{str(long_end)}&rtt=comparison')
    driver.get(url)
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
# driver.get(home_to_metro_link)
# ways = get_ways_to_move(driver)
# print(ways)
# res = get_ways_by_any_points(59.896629,
#                        30.337740,
#                        59.962575,
#                        30.307128, driver)
# print(res)
def get_home_photo(lat, lon, headers):
    link = f'https://2gis.ru/geo/{lat}%2C{lon}?m={lat}%2C{lon}%2F17%2Fp%2F0.04'
    driver.get(link)
    time.sleep(1)
    click_on_photo = driver.find_element(By.CLASS_NAME, "_1dk5lq4")
    click_on_photo.click()
    try:
        time.sleep(1)
        url = driver.find_element(By.XPATH, '//*[@id="photoViewer"]/div/div/div[2]/div[1]/div[1]/div/img').get_attribute('src')
        print(url)
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as response, open('image.png', 'wb') as out_file:
                data = response.read()
                out_file.write(data)
            print("Изображение успешно загружено.")
        except urllib.error.HTTPError as e:
            print("Не удалось загрузить изображение. Код ошибки:", e.code)
    except NoSuchElementException:
        print('Элемент не найден')
lat = '30.332271'
lon = '59.834339'
# link = f'https://2gis.ru/geo/{lat}%2C{lon}?m={lat}%2C{lon}%2F17%2Fp%2F0.04'
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'}
get_home_photo(lat, lon, headers)
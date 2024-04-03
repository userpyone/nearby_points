import time
import json
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
# import fake_headers
from fake_headers import Headers
useragent = UserAgent()
options = webdriver.ChromeOptions()
# options.add_argument(f'user-agent={useragent.random}')
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(
    executable_path=r'C:\Users\ES\PycharmProjects\rent_bot\chromedriver\chromedriver.exe',
    options=options)

header = Headers()

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
        print('На странице нет фото')

lat = '59.838038'
lon = '30.353787'

address = 'Санкт-Петербург, Пулковская ул., 8к4'

# link = f'https://2gis.ru/geo/{lat}%2C{lon}?m={lat}%2C{lon}%2F17%2Fp%2F0.04'
# headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'}
# get_home_photo(address, header.generate())
# print(header.generate())
# ss = 'https://2gis.ru/geo/30.329771%2C59.830982?m=30.331542%2C59.831339%2F17.29%2Fp%2F0.04'
# link = f'https://2gis.ru/geo/{lon}%2C{lat}?m={lon}%2C{lat}%2F17%2Fp%2F0.04'
# print(link)

driver.get("https://wiki.openstreetmap.org/wiki/RU:%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3/%D0%A0%D0%B0%D0%B9%D0%BE%D0%BD%D1%8B")
all_tr_elements = driver.find_elements_by_xpath("//tr")

# Создание списка для хранения данных
data = []

# Обход элементов и извлечение текста
for tr_element in all_tr_elements:
    # Получение всех дочерних элементов <td> в текущем <tr>
    td_elements = tr_element.find_elements_by_tag_name("td")

    # Извлечение текста из каждого <td> и добавление в список данных
    if len(td_elements) >= 2:
        item = {
            "district": td_elements[0].text.encode('utf-8').decode('utf-8'),
            "number": td_elements[1].text.encode('utf-8').decode('utf-8')[1:]
        }
        data.append(item)

# Закрытие браузера
driver.quit()

# Запись данных в JSON файл
with open("spb_districts.json", "w", encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print("Данные успешно записаны в файл data.json")


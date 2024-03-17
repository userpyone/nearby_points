from bs4 import BeautifulSoup
from fake_headers import Headers
from fake_useragent import UserAgent
from selenium import webdriver
import requests
import time
import pickle
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

avito_link = 'https://www.avito.ru/sankt-peterburg/kvartiry/apartamenty-studiya_242m_529et._3712328205'
# address_str = 'Санкт-Петербург, Пулковское ш., 14'
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
    address = driver.find_element_by_class_name('style-item-address__string-wt61A').text
    #Стоимость квартиры
    finding_price = driver.find_elements_by_xpath("//span[@data-marker='item-view/item-price']")
    price = finding_price[1].text.split(' ')[0] + finding_price[1].text.split(' ')[1]
    print('Адрес: ', address)
    print('Стоимость: ', price)

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
        lat = coordinates.split(', ')[0] # широта
        long = coordinates.split(', ')[1] # долгота
        print('Координаты: ', lat, long)
    except:
        print('На странице нет координат!')

    time.sleep(5)

except Exception as e:
    print(e)
finally:
    driver.close()
    driver.quit()

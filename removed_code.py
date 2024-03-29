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

def get_coordinates_by_address(address):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(address)
    if location != None:
        return {'lat': round(location.latitude, 6),
                'lon': round(location.longitude, 6)}
    else:
        print('Location is None!')
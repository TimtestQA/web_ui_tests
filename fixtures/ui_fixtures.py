import os
import allure
import pytest
from selenium import webdriver


def get_driver():
    browser = os.environ["BROWSER"]
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-search-engine-choice-screen")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--allow-insecure-localhost")
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-search-engine-choice-screen")
        options.set_preference("security.ssl.enable_ocsp_stapling", False)
        options.set_preference("security.ssl.enable_false_start", False)
        options.set_preference("security.ssl.require_safe_negotiation", False)
        options.set_preference("security.ssl.treat_unsafe_negotiation_as_broken", False)
        options.set_preference("security.ssl.warn_missing_rfc5746", 0)
        driver = webdriver.Firefox(options=options)
    return driver

@pytest.fixture(autouse=True)
def driver(request):
    driver = get_driver()
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.fixture()
def add_users(request): # Фикстура для добавления юзеров в тест
    user_count = request.param # Принимаем кол-во юзеров из параметров теста
    drivers = [] # Создаем пустой список драйверов, туда будем класть новых юзеров
    for _ in range(user_count):
        driver = get_driver()
        drivers.append(driver) # Тут через цикл мы добавляем новые браузеры в список
    yield drivers # Переходим к тесту
    for driver in drivers: # После теста закрываем все драйверы, которые были созданы
        driver.quit()
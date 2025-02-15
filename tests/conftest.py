import pytest
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@pytest.fixture
def set_up():
    """Инициализация драйвера"""
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    chrome_driver_path = r"C:\Users\golik\PycharmProjects\recource\chromedriver.exe"
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    yield driver  # Возвращаем драйвер для тестов
    driver.quit()


@pytest.fixture(scope="module")
def set_group():
    print("Enter system")
    yield
    print("Exit system")

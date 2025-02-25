import time

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from base.base_class import Base
from utilities.logger import Logger


class Main_page(Base):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Локаторы
    add_item = "(//button[@label='В корзину'])[2]"

    # Геттеры
    def get_add_item(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.add_item)))

    # Действия
    def click_add_item(self):
        self.get_add_item().click()
        print("Товар добавлен из главной в корзину")

    def add_to_cart_main(self):
        with allure.step("Добавляет товар из главной в корзину"):
            Logger.add_start_step(method="add_to_cart_search")
            time.sleep(3)
            self.click_add_item()
            time.sleep(3)
            Logger.add_end_step(url=self.driver.current_url, method="add_to_cart_search")

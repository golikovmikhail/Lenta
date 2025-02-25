import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from base.base_class import Base
from utilities.logger import Logger


class Favorite(Base):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    favorite_button = "//a[@class='favorite-button__link']"
    filter_button = "//span[@aria-label='По популярности']"
    most_expensive_filter = "//li[@aria-label='Сначала дорогие']"
    add_first_item = "(//button[@label='В корзину'])[3]"

    # Getters
    def get_favorite_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.favorite_button)))

    def get_filter_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.filter_button)))

    def get_most_expensive_filter(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.most_expensive_filter)))

    def get_add_first_item(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.add_first_item)))

    # Actions
    def click_favorite_button(self):
        self.get_favorite_button().click()
        print("Открыт раздел 'Избранное'")

    def click_filter_button(self):
        self.get_filter_button().click()
        print("Нажата кнопка 'Фильтр'")

    def click_most_expensive_filter(self):
        self.get_most_expensive_filter().click()
        print("Выбран фильтр 'Сначала дорогие'")

    def click_add_first_item(self):
        self.get_add_first_item().click()
        print("Добавлен самый дорогой товар в корзину")

    # Methods
    def add_to_cart_favorite(self):
        with allure.step("Добавляет товар из избранного в корзину"):
            Logger.add_start_step(method="add_to_cart_favorite")
            print(f"Текущий URL: {self.driver.current_url}")
            time.sleep(3)
            self.click_favorite_button()
            self.click_filter_button()
            self.click_most_expensive_filter()
            time.sleep(3)
            self.click_add_first_item()
            Logger.add_end_step(url=self.driver.current_url, method="add_to_cart_favorite")

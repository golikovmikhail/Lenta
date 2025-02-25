import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from base.base_class import Base
from utilities.logger import Logger


class Search(Base):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Локаторы
    add_item = "//button[@label='В корзину']"
    # alert_deny = "//button[@data-fl-track='click-button-no']"
    # iframe_id = "71-738251"  # ID iframe для модального окна

    # Геттеры
    def get_add_item(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.add_item)))

    # def get_alert_deny(self):
    #     return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.alert_deny)))

    # Действия
    def click_add_item(self):
        self.get_add_item().click()
        print("Товар добавлен в корзину")

    # def close_alert_if_present(self):
    #     """Закрывает пользовательское модальное окно внутри iframe."""
    #
    #     WebDriverWait(self.driver, 10).until(
    #         EC.frame_to_be_available_and_switch_to_it((By.ID, "71-738251"))
    #     )
    #     deny_button = WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, "//button[@data-fl-track='click-button-no']"))
    #     )
    #     deny_button.click()
    #     print("Модальное окно закрыто")
    #     self.driver.switch_to.default_content()

    def add_to_cart_search(self, SKU):
        with allure.step("Добавляет товар из поиска в корзину"):
            Logger.add_start_step(method="add_to_cart_search")
            self.driver.get(f"https://lenta-angular-test13.dev.lenta.tech/search/{SKU}/")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.add_item)))
            # self.close_alert_if_present()
            self.click_add_item()
            Logger.add_end_step(url=self.driver.current_url, method="add_to_cart_search")

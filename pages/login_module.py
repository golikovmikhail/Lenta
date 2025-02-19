import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from base.base_class import Base


class LoginPage(Base):
    url = "https://lenta-angular-test13.dev.lenta.tech/"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    enter_button = "//button[@luautotestlocator='login-button']"
    phone_input = "//input[contains(@class, 'float-label-input')]"
    take_code_button = "//input[@value='Получить код']"
    otp_input = "(//input[@type='text'])[2]"
    choose_delivery_button = "//lu-delivery-switch-button-b2c[@textmain='Доставка']"

    # Getters
    def get_enter_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.enter_button)))

    def get_phone_input(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.phone_input)))

    def get_take_code_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.take_code_button)))

    def get_otp_input(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.otp_input)))

    def get_choose_delivery(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.choose_delivery_button)))


    # Actions
    def click_enter_button(self):
        self.get_enter_button().click()
        print("Нажата кнопка 'Войти'")

    def input_phone(self, phone_number):
        self.get_phone_input().send_keys(phone_number)
        print(f"Введен номер телефона: {phone_number}")

    def click_take_code_button(self):
        self.get_take_code_button().click()
        print("Нажата кнопка 'Получить код'")

    def input_otp(self, otp):
        self.get_otp_input().send_keys(otp)
        print(f"Введен OTP-код: {otp}")

    def choose_delivery(self):
        self.get_choose_delivery().click()
        print("Выбрана доставка'")

    # Methods
    # @pytest.fixture
    def auth(self, phone_number="9439400012", otp="1234"):
        """Авторизация пользователя"""
        self.driver.get(self.url)
        self.driver.maximize_window()
        print(f"Открыта страница: {self.driver.current_url}")
        time.sleep(5)
        self.click_enter_button()
        self.input_phone(phone_number)
        self.click_take_code_button()
        self.input_otp(otp)
        time.sleep(3)  # Ждем завершения авторизации

import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from base.base_class import Base
from utilities.logger import Logger


class Dashboard(Base):
    url = "https://lenta-site-test13.dev.lenta.tech/out/lenta/dashboard"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    profile_button = "//a[@title='Профиль']"
    input_login = "(//input[@tabindex='101'])[2]"
    input_password = "(//input[@name='password'])[2]"
    login_button = "(//button[@type='submit'])[8]"
    orger_button = "//a[@target='_blank']"

    status_button = "//button[@class='status-button']"
    alert_button = "//button[@class='commont-alert-ok']"
    all_button = "//button[@class='pick-all piece-product']"
    picking_warning = "//p[@class='picking-warning']"
    confirm_button = "//button[@class='confirm-correction-confirmation']"
    text_finish = "//span[@id='status-title']"

    # Getters
    def get_profile_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.profile_button)))

    def get_input_login(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.input_login)))

    def get_input_password(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.input_password)))

    def get_login_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.login_button)))

    def get_orger_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.orger_button)))

    def get_status_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.status_button)))

    def get_alert_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.alert_button)))

    def get_all_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.all_button)))

    def get_picking_warning(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.picking_warning)))

    def get_confirm_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.confirm_button)))

    def get_text_finish(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.text_finish)))

    # Actions
    def click_profile_button(self):
        self.get_profile_button().click()
        print("Нажата кнопка 'Войти'")

    def input_input_login(self, login):
        self.get_input_login().send_keys(login)
        print(f"Введен: {login}")

    def input_input_password(self, password):
        self.get_input_password().send_keys(password)
        print(f"Введен: {password}")

    def click_login_button(self):
        self.get_login_button().click()
        print("Нажата кнопка 'Войти'")

    def click_orger_button(self):
        self.get_orger_button().click()
        print("orger_button'")

    def click_status_button(self):
        self.get_status_button().click()
        print("status_button'")

    def click_alert_button(self):
        self.get_alert_button().click()
        print("alert_button'")

    def click_all_button(self):
        self.get_all_button().click()
        print("all_button'")

    def click_picking_warning(self):
        self.get_picking_warning().click()
        print("picking_warning")

    def click_confirm_button(self):
        self.get_confirm_button().click()
        print("confirm_button")

    def verify_text_finish(self, expected_text="Завершен"):
        actual_text = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.text_finish))
        ).text
        assert actual_text == expected_text, f"Ожидалось: '{expected_text}', но получено: '{actual_text}'"
        print(f"Текст '{actual_text}' соответствует ожидаемому значению.")

    # Methods
    # @pytest.fixture
    def auth_dash(self, login="cmf5@utkonos.ru", password="55055505"):
        with allure.step("auth_dash"):
            Logger.add_end_step(url=self.driver.current_url, method="auth_dash")
            self.driver.get(self.url)
            self.driver.maximize_window()
            print(f"Открыта страница: {self.driver.current_url}")
            time.sleep(5)
            self.click_profile_button()
            self.input_input_login(login)
            self.input_input_password(password)
            self.click_login_button()
            time.sleep(3)

    def finish_order(self, order_number):
        with allure.step("finish_order"):
            Logger.add_end_step(url=self.driver.current_url, method="finish_order")
            self.driver.get(f"https://lenta-site-test13.dev.lenta.tech/out/lenta/dashboard?hub={order_number}")
            print(f"Открыта страница: {self.driver.current_url}")
            self.click_orger_button()
            time.sleep(2)
            windows = self.driver.window_handles
            if len(windows) > 1:
                self.driver.switch_to.window(windows[-1])
                print("Переключились на новое окно")
            self.click_status_button()
            self.click_alert_button()
            time.sleep(3)
            self.click_all_button()
            self.click_status_button()
            self.click_alert_button()
            time.sleep(4)
            self.click_status_button()
            self.click_alert_button()
            time.sleep(4)
            self.click_status_button()
            time.sleep(3)
            self.click_status_button()
            self.click_confirm_button()
            time.sleep(5)
            self.verify_text_finish()


import time
import allure
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from base.base_class import Base
from utilities.logger import Logger
from selenium.webdriver.common.action_chains import ActionChains


class Checkout(Base):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    go_to_cart_button = "//a[@class='cart-button__link']"
    to_checkout_button = "//button[@luautotestlocator='basket-checkout-btn']"
    checkout_make_order = "//button[@luautotestlocator='checkout-make-order']"
    order_created_button = "//button[@label='Понятно']"
    order_number = "//div[@class='order-id']"
    input_promo = "(//input[@type='text'])[2]"

    # Getters
    def get_go_to_cart_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.go_to_cart_button)))

    def get_to_checkout_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.to_checkout_button)))

    def get_checkout_make_order(self):
        return WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.checkout_make_order)))

    def get_order_created_button(self):
        return WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, self.order_created_button)))

    def get_order_number(self):
        return WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, self.order_number)))

    def get_input_promo(self):
        return WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, self.input_promo)))

    # Actions
    def click_go_to_cart(self):
        self.get_go_to_cart_button().click()
        print("Перешли в корзину")

    def click_to_checkout(self):
        self.get_to_checkout_button().click()
        print("Перешли к оформлению заказа")

    def click_checkout_make_order(self):
        self.get_checkout_make_order().click()
        print("Оформить заказ")

    def click_order_created_button(self):
        self.get_order_created_button().click()
        print("Заказ оформлен")

    def get_text_order_number(self):
        """Получает и проверяет номер заказа без символа '№'"""
        order_number_text = self.get_order_number().text.strip()

        assert order_number_text, "Ошибка: номер заказа не получен!"  # Проверяем, что номер заказа не пустой

        # Удаляем все нецифровые символы, оставляя только цифры
        order_number_clean = "".join(filter(str.isdigit, order_number_text))

        assert order_number_clean, "Ошибка: после обработки номер заказа отсутствует!"  # Проверяем, что остались цифры

        print(f"Номер заказа: {order_number_clean}")
        return order_number_clean

    def input_input_promo(self):
        # self.get_input_promo().click()
        time.sleep(3)
        self.get_input_promo().send_keys("PROMO25")
        print("Введен промокод")
        time.sleep(3)
        self.get_input_promo().send_keys(Keys.RETURN)

    # Methods
    def complete_order(self):
        with allure.step("Проходит весь процесс оформления заказа"):
            Logger.add_start_step(method="complete_order")
            time.sleep(3)
            self.click_go_to_cart()
            self.click_to_checkout()
            for _ in range(4):  # Не более 4 попыток
                try:
                    btn = self.get_checkout_make_order()
                    if btn.is_enabled():
                        btn.click()
                        print("Оформить заказ - нажатие выполнено")
                        time.sleep(2)
                    else:
                        print("Кнопка 'Оформить заказ' не активна, пропускаем...")
                        break
                except Exception as e:
                    print(f"Ошибка при нажатии на 'Оформить заказ': {e}")
                    break  # Если ошибка - выходим из цикла
            time.sleep(15)
            self.click_order_created_button()
            Logger.add_end_step(url=self.driver.current_url, method="complete_order")
            return self.get_text_order_number()

    def complete_order_promo(self):
        with allure.step("Проходит весь процесс оформления заказа с использованием промокода"):
            Logger.add_start_step(method="complete_order")
            time.sleep(3)
            self.click_go_to_cart()
            time.sleep(3)
            self.input_input_promo()
            time.sleep(3)
            self.click_to_checkout()

            # Проверяем, можно ли нажать "Оформить заказ"
            for _ in range(4):  # Не более 4 попыток
                try:
                    btn = self.get_checkout_make_order()
                    if btn.is_enabled():
                        btn.click()
                        print("Оформить заказ - нажатие выполнено")
                        time.sleep(2)
                    else:
                        print("Кнопка 'Оформить заказ' не активна, пропускаем...")
                        break
                except Exception as e:
                    print(f"Ошибка при нажатии на 'Оформить заказ': {e}")
                    break  # Если ошибка - выходим из цикла

            time.sleep(15)
            self.click_order_created_button()
            Logger.add_end_step(url=self.driver.current_url, method="complete_order")
            return self.get_text_order_number()


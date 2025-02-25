import pytest
import allure
from pages.complete_order import Checkout
from pages.dashboard import Dashboard
from pages.login import LoginPage
from pages.main_page import Main_page


@pytest.mark.smoke
@allure.description("Создание заказа с самовывозом и промокодом")
def test_full_order(set_up):
    driver = set_up

    login = LoginPage(driver)
    login.auth()

    main = Main_page(driver)
    main.add_to_cart_main()

    ch = Checkout(driver)
    order_number = ch.complete_order_promo()

    print(f"Тест завершен успешно, заказ № {order_number}")

    dash = Dashboard(driver)
    dash.auth_dash()
    dash.finish_order(order_number)

# pytest -m smoke -s
# python -m pytest --alluredir=test_results/tests/
# python -m pytest --alluredir=test_results/
# allure serve test_results/tests/
# allure serve test_results/

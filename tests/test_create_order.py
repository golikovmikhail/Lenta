import pytest

from pages.finish_order import Checkout
from pages.favorite_page import Favorite
from pages.login_module import LoginPage


@pytest.mark.smoke
def test_full_order(set_up):
    """Полный сценарий теста"""
    driver = set_up

    try:
        login = LoginPage(driver)
        login.auth()

        fav = Favorite(driver)
        fav.add_to_cart_favorite()

        checkout = Checkout(driver)
        order_number = checkout.complete_order()

        print(f"Тест завершен успешно, заказ № {order_number}")
    except Exception as e:
        print(f"Тест не завершен успешно. Ошибка: {e}")

#pytest -m smoke

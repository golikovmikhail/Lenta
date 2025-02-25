import pytest
import allure
import logging
from pages.dashboard import Dashboard
from pages.order_import import Import

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.smoke
@allure.description("Создание заказа с самовывозом, промокодом и оплатой")
def test_import_order(set_up):
    driver = set_up
    im = Import()

    # Загружаем order_id и phone_number
    order_id, phone_number = im.load_order_details()

    try:
        # Отправляем заказ
        response = im.send_order(order_id, phone_number)

        # Проверяем, что запрос успешен
        if "result" in response:
            api_order_id = response["result"]["order_id"]
            logger.info(f"Тест завершен успешно, заказ № {api_order_id}")

            # Сохраняем новые order_id и phone_number
            im.save_order_details(order_id + 1, str(int(phone_number) + 1), api_order_id)

            # Авторизация и завершение заказа в Dashboard
            dash = Dashboard(driver)
            dash.auth_dash()
            dash.finish_order(api_order_id)

            # Здесь можно добавить шаги по оплате
            # Например: dash.process_payment(api_order_id)

        else:
            # Если ошибка при создании заказа, проверяем детали ошибки
            error_code = response.get("error", {}).get("code")
            if error_code == 129:
                # Ошибка 129: Интервал времени закрыт, пробуем новый интервал
                logger.warning("Ошибка 129: Интервал времени закрыт. Попробуем новый интервал.")
                new_interval = response["error"]["data"]["pickup"][0]["id"]
                response = im.send_order(order_id, phone_number, delivery_interval_id=new_interval)

                # Проверяем успешность повторной попытки
                if "result" in response:
                    api_order_id = response["result"]["order_id"]
                    logger.info(f"Тест завершен успешно с новым интервалом, заказ № {api_order_id}")
                    im.save_order_details(order_id + 1, str(int(phone_number) + 1), api_order_id)
                    dash = Dashboard(driver)
                    dash.auth_dash()
                    dash.finish_order(api_order_id)
                else:
                    logger.error("Ошибка при создании заказа с новым интервалом: %s", response)
                    pytest.fail(f"Не удалось создать заказ с новым интервалом. Ответ от API: {response}")

            else:
                logger.error("Ошибка при создании заказа: %s", response)
                pytest.fail(f"Не удалось создать заказ. Ответ от API: {response}")

    except Exception as e:
        logger.error(f"Ошибка при отправке запроса: {e}")
        pytest.fail(f"Не удалось создать заказ. Ошибка: {e}")

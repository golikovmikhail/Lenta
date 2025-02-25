import requests
import json
import time
import uuid
import random


class Import:
    @staticmethod
    def generate_unique_id():
        # Генерация уникального ID для запроса
        return str(uuid.uuid4())

    @staticmethod
    def generate_random_phone_number():
        # Генерация случайного номера телефона, начинающегося на 7943
        return f"7943{random.randint(1000000, 9999999)}"

    @staticmethod
    def generate_random_order_id():
        # Генерация случайного orderId, например, "test12345"
        return f"test{random.randint(1000, 9999)}"

    @staticmethod
    def send_order(order_id, phone_number, delivery_interval_id=None, request_id=None):
        url = 'https://lenta-site-test13.dev.lenta.tech/jrpc/OrderImport'
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json',
            'Deviceid': '123123123',
            'Marketingpartnerkey': 'mp75-fake-key',
            'X-Request-Id': request_id or Import.generate_unique_id(),  # Генерация нового уникального X-Request-Id
            'X-Retail-Brand': 'lo',
            'Cookie': 'SOURCE_ID_time=2025-02-24%2019%3A54%3A33; Utk_SssTkn=570EF1C085F98BFA50615F54F84F1A79'
        }

        data = {
            "id": Import.generate_unique_id(),  # Генерация нового уникального id для запроса
            "jsonrpc": "2.0",
            "method": "OrderImport",
            "params": {
                "deliveryIntervalId": delivery_interval_id or "22428040",
                "deliveryStore": "0124",
                "information": f"Номер заказа Яндекс.Еды: test13. Код выдачи заказа: 4321.",
                "intervalType": "pickup_express",
                "items": [
                    {
                        "amount": 1,
                        "cost": 3099.99,
                        "cost_regular": 3263.19,
                        "sku": 262577,
                        "unit": "ST",
                        "unit_price": 3099.99,
                        "unit_price_regular": 3263.19
                    }
                ],
                "orderId": order_id,  # Используем случайно сгенерированный orderId
                "replaceCommunication": 4,
                "sumLimitMultiplier": 1.3,
                "timestamp": int(time.time()),
                "userAdditionalPhone": "4321",
                "userKey": f"yandex_food_{phone_number}_4321",
                "userPhone": phone_number,  # Используем случайный номер телефона
                "userSurname": "Андрей"
            }
        }

        response = requests.post(url, headers=headers, json=data)
        return response.json()

    @staticmethod
    def save_order_details(order_id, phone_number, api_order_id):
        with open("order_info.txt", "w") as file:
            file.write(f"orderId={order_id}\nphoneNumber={phone_number}\napiOrderId={api_order_id}")

    @staticmethod
    def load_order_details():
        try:
            with open("order_info.txt", "r") as file:
                lines = file.readlines()
                order_id = int(lines[0].strip().split('=')[1]) + 1  # Увеличиваем order_id
                phone_number = lines[1].strip().split('=')[1]  # Получаем телефон как строку
                phone_number = str(int(phone_number) + 1)  # Увеличиваем номер телефона
                return order_id, phone_number
        except FileNotFoundError:
            return 123, "79439410015"  # Значения по умолчанию

    @staticmethod
    def main():
        order_id, phone_number = Import.load_order_details()

        attempt = 0
        max_attempts = 10  # Максимальное количество попыток

        while attempt < max_attempts:
            request_id = Import.generate_unique_id()  # Генерация нового уникального Request Id для каждой попытки
            phone_number = Import.generate_random_phone_number()  # Генерация случайного номера телефона
            order_id = Import.generate_random_order_id()  # Генерация случайного orderId
            print(f"Попытка №{attempt + 1} создать заказ с orderId={order_id} и phoneNumber={phone_number}")

            # Отправляем запрос с новыми параметрами
            response = Import.send_order(order_id, phone_number, request_id=request_id)

            if "result" in response:
                api_order_id = response["result"]["order_id"]
                print(f"Заказ успешно создан! Order ID: {api_order_id}")
                Import.save_order_details(order_id, phone_number, api_order_id)  # Сохраняем обновленные данные
                break  # Завершаем цикл, если заказ успешно создан
            else:
                print("Ошибка при создании заказа:", response)
                if "error" in response and response["error"]["code"] == 129:
                    print("Ошибка 129: Интервал закрыт. Берём предложенный интервал...")
                    new_interval = response["error"]["data"]["pickup"][0]["id"]
                    response = Import.send_order(order_id, phone_number, delivery_interval_id=new_interval,
                                                 request_id=request_id)
                    if "result" in response:
                        api_order_id = response["result"]["order_id"]
                        print(f"Заказ успешно создан с новым интервалом! Order ID: {api_order_id}")
                        Import.save_order_details(order_id, phone_number, api_order_id)  # Сохраняем обновленные данные
                        break  # Завершаем цикл, если заказ успешно создан с новым интервалом

                # Увеличиваем order_id и phone_number для следующей попытки
                order_id += 1
                phone_number = str(int(phone_number) + 1)

            attempt += 1

        if attempt == max_attempts:
            print("Не удалось создать заказ за максимальное количество попыток.")


if __name__ == "__main__":
    Import.main()

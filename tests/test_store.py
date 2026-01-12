import allure
import pytest

from src.models.api_response import ApiResponse
from src.models.order import InventoryResponse, Order


@allure.epic("Petstore")
@allure.feature("Store")
class TestsStore:

    @allure.title("Получить все статусы товаров и количество товаров по данным статусам")
    def test_get_product_statuses(self, authorized_user, store_api):
        response = store_api.get_inventory()

        with allure.step("Успешный статус код ответа"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели InventoryResponse"):
            inventory = InventoryResponse.model_validate(response.json())

        with allure.step("Значение по каждому статусу больше нуля"):
            for key, value in inventory.root.items():
                assert value > 0, f"Значение по статусу {key} меньше нуля"

    @allure.title("Создание нового заказа на животного с заполнением всех полей")
    def test_post_create_order_all_fields(self, generate_body_order, delete_order_after_test,
                                          create_new_pet, authorized_user, store_api):
        order_body = generate_body_order(order_id=True, quantity=True, ship_date=True, status=True, complete=True)
        order_body['petId'] = create_new_pet['id']
        response = store_api.post_add_new_order(body=order_body)

        with allure.step("Успешный статус код ответа"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели Order"):
            Order.model_validate(response.json())

        with allure.step("Сверка отправленных данных с полученными"):
            order_response_body = response.json()
            assert order_response_body["id"] == order_body["id"]
            assert order_response_body["petId"] == order_body["petId"]
            assert order_response_body["quantity"] == order_body["quantity"]
            assert order_response_body["shipDate"] == order_body["shipDate"]
            assert order_response_body["status"] == order_body["status"]
            assert order_response_body["complete"] == order_body["complete"]

        delete_order_after_test['id'] = order_response_body["id"]

    @pytest.mark.parametrize("status,", ["placed", "approved", "delivered"])
    @allure.title("Создание нового заказа на животного со статуом {status}")
    def test_post_create_order_with_status(self, generate_body_order, delete_order_after_test,
                                           create_new_pet, authorized_user, status, store_api):
        order_body = {
            'petId': create_new_pet['id'],
            'status': status
        }
        response = store_api.post_add_new_order(body=order_body)

        with allure.step("Успешный статус код ответа"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели Order"):
            Order.model_validate(response.json())

        with allure.step("Статус питомца соответствует указанному статусу при создании"):
            order_response_body = response.json()
            assert order_response_body["status"] == order_body["status"]

        delete_order_after_test['id'] = order_response_body["id"]

    @pytest.mark.parametrize("date,", ["test", True, [], 25])
    @allure.title("Создание нового заказа на животного указав дату создания не в верном формате: {date}")
    def test_post_create_order_invalid_format_date(self, generate_body_order, delete_order_after_test,
                                                   create_new_pet, authorized_user, date, store_api):
        order_body = {
            'petId': create_new_pet['id'],
            'shipDate': date
        }
        response = store_api.post_add_new_order(body=order_body)

        with allure.step("Статус код ответа с ошибкой 400"):
            assert response.status_code == 400, f"Не верный статус ответа: {response.text}"

    @allure.title("Получить информацию о заказе по id")
    def test_get_order_by_id(self, create_new_order, store_api):
        order_body = create_new_order
        response = store_api.get_order_by_id(order_id=order_body["id"])

        with allure.step("Успешный статус код ответа"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели Order"):
            order_response = Order.model_validate(response.json())

        with allure.step("В ответе содержится информация о том питомце, чей id передавался в запросе"):
            assert order_response.id == order_body["id"]
            assert order_response.petId == order_body["petId"]

    @pytest.mark.parametrize("invalid_id,", ["test", True, [], None])
    @allure.title("Отправить запрос на получение заказа по id c неверным типом данных в id")
    def test_get_order_by_invalid_id(self, invalid_id, store_api):
        response = store_api.get_order_by_id(order_id=invalid_id)

        with allure.step("Статус код с ошибкой 400 или 404"):
            assert response.status_code in (400, 404), f"Не верный статус ответа: {response.text}"

    @allure.title("Отправить запрос на получение заказа по id c несуществующим id")
    def test_get_order_by_non_existent_id(self, create_new_order, store_api):
        order_id = create_new_order["id"]
        store_api.delete_order(order_id=order_id)

        response = store_api.get_order_by_id(order_id=order_id)

        with allure.step("Статус код с ошибкой 404"):
            assert response.status_code == 404, f"Не верный статус ответа: {response.text}"

    @allure.title("Удалить заказ")
    def test_delete_order_by_id(self, create_new_order, store_api):
        order_id = create_new_order["id"]
        response = store_api.delete_order(order_id=order_id)

        with allure.step("Успешный статус код ответа"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели ApiResponse"):
            response = ApiResponse.model_validate(response.json())
            assert response.code == 200
            assert response.type == "unknown"
            assert response.message == str(order_id)

    @allure.title("Удалить заказ, которого не существует в системе")
    def test_delete_order_by_id_does_not_exist(self, create_new_order, store_api):
        order_id = create_new_order["id"]
        store_api.delete_order(order_id=order_id)

        with allure.step("Совершаем попытку удалить, уже удаленный заказ"):
            response = store_api.delete_order(order_id=order_id)

        with allure.step("Статус код с ошибкой 404"):
            assert response.status_code == 404, f"Не верный статус ответа: {response.text}"
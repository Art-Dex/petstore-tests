import os

import allure
from requests import Response

from src.constants.store_api_routes import StoreAPIRoutes
from src.http_client import HttpClient


class StoreAPI:
    def __init__(self):
        self.header = {'Accept': 'application/json'}
        self._client = HttpClient(base_url=os.getenv("API_BASE_URL"))
        self._get_inventory_rout = StoreAPIRoutes.GET_INVENTORY
        self._post_order_rout = StoreAPIRoutes.POST_ORDER
        self._get_and_delete_order_by_id_rout = StoreAPIRoutes.GET_AND_DELETE_ORDER_BY_ID

    @allure.step('Получить количество товаров по каждому статусу')
    def get_inventory(self) -> Response:
        return self._client.get(path=self._get_inventory_rout, header=self.header)

    @allure.step('Оформить новый заказ на питомца')
    def post_add_new_order(self, body: dict) -> Response:
        return self._client.post(path=self._post_order_rout, body=body, header=self.header)

    @allure.step('Получить заказ на питомца по id')
    def get_order_by_id(self, order_id: int | None) -> Response:
        url_path = self._get_and_delete_order_by_id_rout.format(order_id=order_id)
        return self._client.get(path=url_path, header=self.header)

    @allure.step('Удалить заказ на питомца')
    def delete_order(self, order_id: int | None) -> Response:
        url_path = self._get_and_delete_order_by_id_rout.format(order_id=order_id)
        return self._client.delete(path=url_path, header=self.header)
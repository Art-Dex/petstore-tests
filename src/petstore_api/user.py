import os
import allure

from src.http_client import HttpClient
from requests import Response
from src.constants.user_api_routes import UserAPIRoutes


class UserAPI:
    def __init__(self):
        self.header = {'Accept': 'application/json'}
        self._client = HttpClient(base_url=os.getenv("API_BASE_URL"))
        self._create_user_rout = UserAPIRoutes.CREATE_USER
        self._create_users_with_list_rout = UserAPIRoutes.CREATE_USER_WITH_LIST
        self._get_updates_deletes_user_rout = UserAPIRoutes.GET_UPDATES_DELETES_USER_BY_USERNAME
        self._get_user_login_rout = UserAPIRoutes.GET_LOGIN_USER
        self._get_user_logout_rout = UserAPIRoutes.GET_LOGOUT_USER

    @allure.step('Создание нового пользователя')
    def post_create_new_user(self, body: dict | None) -> Response:
        return self._client.post(path=self._create_user_rout, body=body, header=self.header)

    @allure.step('Создание новых пользователей на основе заданного входного списка')
    def post_create_new_users_with_list(self, body: list | None) -> Response:
        return self._client.post(path=self._create_users_with_list_rout, body=body, header=self.header)

    @allure.step('Получить пользователя по имени пользователя')
    def get_user_by_username(self, username: str | None) -> Response:
        url_path = self._get_updates_deletes_user_rout.format(username=username)
        return self._client.get(path=url_path, header=self.header)

    @allure.step('Обновить информацию о пользователе')
    def put_updates_user(self, username: str | None, body: dict | None) -> Response:
        url_path = self._get_updates_deletes_user_rout.format(username=username)
        return self._client.put(path=url_path, body=body, header=self.header)

    @allure.step('Удаление пользователя')
    def delete_user(self, username: str | None) -> Response:
        url_path = self._get_updates_deletes_user_rout.format(username=username)
        return self._client.delete(path=url_path, header=self.header)

    @allure.step('Авторизоваться под пользователем')
    def get_user_login(self, **kwargs):
        return self._client.get(path=self._get_user_login_rout, header=self.header, params=kwargs)

    @allure.step('Разлогинится под пользователем')
    def get_user_logout(self):
        return self._client.get(path=self._get_user_logout_rout, header=self.header)
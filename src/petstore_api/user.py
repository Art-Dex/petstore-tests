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

    @allure.step('Создание нового пользователя')
    def post_create_new_user(self, body: dict) -> Response:
        return self._client.post(path=self._create_user_rout, body=body, header=self.header)
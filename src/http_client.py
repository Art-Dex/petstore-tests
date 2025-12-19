import requests
import allure


class HttpClient:
    def __init__(self, base_url: str) -> None:
        """
        Инициализация клиента.

        Args:
            base_url: базовый URL API
        """
        self.base_url = base_url.rstrip('/')

    def _url(self, path: str) -> str:
        """
        Построить полный URL из базового URL и относительного пути.

        Args:
            path: относительный путь

        Returns:
            str: полный URL
        """
        return f"{self.base_url}/{path.lstrip('/')}"

    def request(self, method, path, params=None, body=None, headers=None, data=None):
        """
        Универсальный метод отправки HTTP-запроса.

        Args:
            method: HTTP-метод: "GET", "POST", "PUT", "DELETE", "PATCH"
            path: относительный путь ресурса
            params: query-параметры
            body: тело запроса в формате JSON
            headers: дополнительные HTTP-заголовки
            data: Тело запроса в формате form-encoded или бинарные данные.
                Используется для отправки форм или произвольных данных.
                Для form-encoded данных устанавливается заголовок
                Content-Type: application/x-www-form-urlencoded.
                Взаимоисключающий параметр с `body`.
        Returns:
            объект requests.Response для дальнейшей проверки
        """
        url = self._url(path)

        resp = requests.request(
            method=method,
            url=url,
            params=params,
            json=body,
            data=data,
            headers=headers
        )

        if resp.status_code >= 400:
            allure.attach(resp.text, "Response body", allure.attachment_type.TEXT)

        return resp

    @allure.step('Отправить GET запрос к "{path}"')
    def get(self, path: str, params: dict = None, header: dict = None) -> requests.Response:
        return self.request(method="GET", path=path, params=params, headers=header)

    @allure.step('Отправить POST запрос к "{path}"')
    def post(self, path: str, body: dict = None, params: dict = None,
             header: dict = None, data=None) -> requests.Response:
        resp = self.request(method="POST", path=path, params=params, body=body, headers=header, data=data)
        return resp

    @allure.step('Отправить PUT запрос к "{path}"')
    def put(self, path: str, body: dict = None, params: dict = None, header: dict = None) -> requests.Response:
        resp = self.request(method="PUT", path=path, params=params, body=body, headers=header)
        return resp

    @allure.step('Отправить DELETE запрос к "{path}"')
    def delete(self, path: str, params: dict = None, header: dict = None) -> requests.Response:
        resp = self.request(method="DELETE", path=path, params=params, headers=header)
        return resp

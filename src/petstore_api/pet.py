import os
import allure

from src.http_client import HttpClient
from requests import Response
from src.constants.pet_api_routes import PetAPIRoutes


class PetAPI:
    def __init__(self):
        self.header = {'Accept': 'application/json'}
        self._client = HttpClient(base_url=os.getenv("API_BASE_URL"))
        self._add_or_update_pet_rout = PetAPIRoutes.ADD_OR_UPDATE_PET
        self._get_list_pets_by_status_rout = PetAPIRoutes.GET_A_LIST_OF_PETS_BY_STATUS
        self._get_list_pets_by_tags_rout = PetAPIRoutes.GET_A_LIST_OF_PETS_BY_TAGS
        self._get_pet_by_id_rout = PetAPIRoutes.GET_PET_BY_ID
        self._update_pet_with_form_date_rout = PetAPIRoutes.UPDATES_PET_IN_THE_STORE_WITH_FORM_DATA
        self._delete_pet_rout = PetAPIRoutes.DELETES_A_PET
        self._upload_an_image_rout = PetAPIRoutes.UPLOADS_AN_IMAGE

    @allure.step('Создание нового питомца')
    def post_add_new_pet(self, body: dict) -> Response:
        return self._client.post(path=self._add_or_update_pet_rout, body=body, header=self.header)

    @allure.step('Изменить данные существуещего питомца')
    def put_update_pet(self, body: dict) -> Response:
        return self._client.put(path=self._add_or_update_pet_rout, body=body, header=self.header)

    @allure.step('Получить список питомцев по статусу')
    def get_list_pets_by_status(self, **kwargs) -> Response:
        return self._client.get(path=self._get_list_pets_by_status_rout, params=kwargs, header=self.header)

    @allure.step('Получить список питомцев по тегам')
    def get_list_pets_by_tags(self, **kwargs) -> Response:
        return self._client.get(path=self._get_list_pets_by_tags_rout, params=kwargs, header=self.header)

    @allure.step('Получить питомца по id')
    def get_pet_by_id(self, pet_id: int | None) -> Response:
        url_path = self._get_pet_by_id_rout.format(pet_id=pet_id)
        return self._client.get(path=url_path, header=self.header)

    @allure.step('Обновить информацию о питомце на основе данных из формы')
    def post_update_pet_with_form(self, pet_id: int | None, **kwargs) -> Response:
        url_path = self._update_pet_with_form_date_rout.format(pet_id=pet_id)
        return self._client.post(path=url_path, params=kwargs, header=self.header)

    @allure.step('Удаление питомца')
    def delete_pet(self, pet_id: int | None) -> Response:
        url_path = self._delete_pet_rout.format(pet_id=pet_id)
        return self._client.delete(path=url_path, header=self.header)

    @allure.step("Загрузить изображение питомца")
    def post_upload_pet_image(self, pet_id: int, file_path: str, **kwargs):
        url_path = self._upload_an_image_rout.format(pet_id=pet_id)
        header = dict(self.header, **{'Content-Type': 'application/octet-stream'})
        with open(file_path, "rb") as file:
            file_data = file.read()

        return self._client.post(path=url_path, header=header, data=file_data, params=kwargs)

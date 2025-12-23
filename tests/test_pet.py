import allure
import pytest

from src.data_generator.data_generator import generate_randon_status_pet, generate_randon_name
from src.models.pet import Pet, FieldPetStatus
from src.petstore_api.pet import PetAPI


@allure.epic("Petstore")
@allure.feature("Pet")
class TestsPet:
    pet_api = PetAPI()

    @allure.title("Создание нового питомца с заполнением всех полей")
    def test_post_create_pet_all_fields(self, generate_body_pet, delete_pet_after_test):
        pet_body = generate_body_pet(id=True, name=True, photoUrls=True, status=True, tags=True, category=True)
        response = self.pet_api.post_add_new_pet(body=pet_body)

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели Pet"):
            pet_response = Pet.model_validate(response.json())

        with allure.step("Сверка отправленных данных с полученными"):
            assert pet_response.id == pet_body["id"]
            assert pet_response.name == pet_body["name"]
            assert pet_response.photoUrls == pet_body["photoUrls"]
            assert pet_response.status == pet_body["status"]
            assert pet_response.tags[0].model_dump() == pet_body["tags"][0]
            assert pet_response.category.model_dump() == pet_body["category"]

        with allure.step("Удаление питомца после теста"):
            delete_pet_after_test['id'] = pet_response.id

    @allure.title("Создание нового питомца с заполнением только обязательных полей")
    def test_post_create_pet_with_necessary_fields(self, generate_body_pet, delete_pet_after_test):
        pet_body = generate_body_pet(name=True, photoUrls=True)
        response = self.pet_api.post_add_new_pet(body=pet_body)

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"
        # 500 ошибка, обязательные поля в схеме не соответствуют дейстивительности, id считается как обязательный
        # параметр

        with allure.step("Ответ соответствует модели Pet"):
            pet_response = Pet.model_validate(response.json())

        with allure.step("Сверка отправленных данных с полученными"):
            assert pet_response.name == pet_body["name"]
            assert pet_response.photoUrls == pet_body["photoUrls"]

        with allure.step("Удаление питомца после теста"):
            delete_pet_after_test['id'] = pet_response.id

    @pytest.mark.parametrize("status,", ["available", "pending", "sold"])
    @allure.title("Создание нового питомца со статуом {status}")
    def test_post_create_pet_all_status(self, generate_body_pet, delete_pet_after_test, status):
        pet_body = generate_body_pet(name=True, photoUrls=True, id=True)
        pet_body['status'] = status
        response = self.pet_api.post_add_new_pet(body=pet_body)

        with allure.step("Проверяем статус код"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели Pet"):
            pet_response = Pet.model_validate(response.json())

        with allure.step("Сверка статуса питомца"):
            assert pet_response.status == pet_body["status"]

        with allure.step("Удаление питомца после теста"):
            delete_pet_after_test['id'] = pet_response.id

    @pytest.mark.parametrize(
        "missing_field, body_kwargs",
        [
            (
                    "name",
                    dict(photoUrls=True, id=True)
            ),
            (
                    "photoUrls",
                    dict(name=True, id=True)
            ),
        ]
    )
    @allure.title("Cоздание питомца без обязательного поля '{missing_field}'")
    def test_post_create_pet_missing_required_fields(self, generate_body_pet, missing_field, body_kwargs):
        pet_body = generate_body_pet(**body_kwargs)
        response = self.pet_api.post_add_new_pet(body=pet_body)

        with allure.step(f"Проверка статус кода при отсутствии поля '{missing_field}'"):
            assert response.status_code in (400, 422), f"Не верный статус ответа: {response.text}"

    @allure.title("Изменение всех полей в данных о питомце")
    def test_put_update_pet_all_fields(self, generate_body_pet, create_new_pet):
        pet_id = create_new_pet['id']
        pet_body = generate_body_pet(name=True, photoUrls=True, status=True, tags=True, category=True)
        pet_body['id'] = pet_id
        response = self.pet_api.put_update_pet(body=pet_body)

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели Pet"):
            pet_response = Pet.model_validate(response.json())

        with allure.step("Сверка отправленных данных с полученными"):
            assert pet_response.name == pet_body["name"]
            assert pet_response.photoUrls == pet_body["photoUrls"]
            assert pet_response.status == pet_body["status"]
            assert pet_response.tags[0].model_dump() == pet_body["tags"][0]
            assert pet_response.category.model_dump() == pet_body["category"]

    @pytest.mark.parametrize(
        "missing, body_kwargs",
        [
            (
                    "name",
                    dict(name=True)
            ),
            (
                    "photoUrls",
                    dict(photoUrls=True)
            ),
            (
                    "category",
                    dict(category=True)
            ),
            (
                    "tags",
                    dict(tags=True)
            ),
            (
                    "status",
                    dict(status=True)
            ),
        ]
    )
    @allure.title("Изменение  поля '{missing}' в данных о питомце")
    def test_put_update_pet_one_field(self, generate_body_pet, create_new_pet, missing, body_kwargs):
        pet_id = create_new_pet['id']
        pet_body = generate_body_pet(**body_kwargs)
        pet_body['id'] = pet_id
        response = self.pet_api.put_update_pet(body=pet_body)

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Проверка, что поле изменилось"):
            assert response.json()[missing] == pet_body[missing]

    @allure.title("Изменение данных о питомце без передачи id")
    def test_put_update_pet_without_id(self, generate_body_pet, create_new_pet):
        pet_body = generate_body_pet(name=True, photoUrls=True, status=True, tags=True, category=True)
        response = self.pet_api.put_update_pet(body=pet_body)

        with allure.step("Проверка статус кода"):
            assert response.status_code in (400, 404), f"Не верный статус ответа: {response.text}"

    @pytest.mark.parametrize("status,", ["available", "pending", "sold"])
    @allure.title("Вывести список всех питомцев по статусу {status}")
    def test_get_list_pets_by_status(self, status):

        response = self.pet_api.get_list_pets_by_status(status=status)

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, "Не верный статус ответа: {response.text}"

        with allure.step("Проверка, что все питомцы в ответе содержат верный статус"):
            for pet in response.json():
                assert pet['status'] == status

    @allure.title("Вывести список всех питомцев по несуществующему статусу")
    def test_get_list_pets_in_minor_status(self):
        response = self.pet_api.get_list_pets_by_status(status="status")

        with allure.step("Проверка статус кода"):
            assert response.status_code == 400, "Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели FieldPeyStatus"):
            expected = FieldPetStatus.from_invalid_status("status")
            pet_response = FieldPetStatus.model_validate(response.json())
            assert pet_response.message == expected.message

    @allure.title("Вывести список всех питомцев по тегу")
    def test_get_list_pets_by_tag(self, create_new_pet):
        tag_dict = create_new_pet["tags"][0]

        response = self.pet_api.get_list_pets_by_tags(tags=tag_dict['name'])

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, "Не верный статус ответа: {response.text}"

        with allure.step("Проверка, что все питомцы в ответе содержат верный тег"):
            for pet in response.json():
                assert pet["tags"][0]["name"] == tag_dict['name']

    @allure.title("Получить информацию о питомце по id")
    def test_get_pet_by_id(self, create_new_pet):
        pet_body = create_new_pet
        response = self.pet_api.get_pet_by_id(pet_id=pet_body["id"])

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, "Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели Pet"):
            pet_response = Pet.model_validate(response.json())

        with allure.step("В ответе содержится информация о том питомце, чей id передавался в запросе"):
            assert pet_response.id == pet_body["id"]
            assert pet_response.name == pet_body["name"]

    @allure.title("Отправить запрос на получение питомца по id c неверным типом данных в id")
    def test_get_pet_by_invalid_id(self):

        response = self.pet_api.get_pet_by_id(pet_id=None)

        with allure.step("Проверка статус кода"):
            assert response.status_code == 400, "Не верный статус ответа: {response.text}"

    @allure.title("Обновить имя и статус питомца через форму")
    def test_post_update_pet_name_and_status_with_form(self, create_new_pet):
        pet_body = create_new_pet
        name = generate_randon_name()
        status = generate_randon_status_pet()
        response = self.pet_api.post_update_pet_with_form(pet_id=pet_body["id"], name=name, status=status)

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, "Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели Pet"):
            pet_response = Pet.model_validate(response.json())

        with allure.step("Проверка совпадения значения name, с указанным значением в форме"):
            assert pet_response.name == name

        with allure.step("Проверка совпадения значения status, с указанным значением в форме"):
            assert pet_response.status == status

    @allure.title("Обновить только имя питомца через форму")
    def test_post_update_pet_name_with_form(self, create_new_pet):
        pet_body = create_new_pet
        name = generate_randon_name()
        response = self.pet_api.post_update_pet_with_form(pet_id=pet_body["id"], name=name)

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, "Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели Pet"):
            pet_response = Pet.model_validate(response.json())

        with allure.step("Проверка совпадения значения name, с указанным значением в форме"):
            assert pet_response.name == name

    @allure.title("Обновить иня и  статус питомца через форму, указав несуществущий статус")
    def test_post_update_pet_invalid_status_with_form(self, create_new_pet):
        pet_body = create_new_pet
        name = generate_randon_name()
        status = generate_randon_name()
        response = self.pet_api.post_update_pet_with_form(pet_id=pet_body["id"], name=name, status=status)

        with allure.step("Проверка статус кода"):
            assert response.status_code == 400, "Не верный статус ответа: {response.text}"

    @allure.title("Удалить питомца")
    def test_delete_pet_by_id(self, create_new_pet):
        pet_body = create_new_pet
        response = self.pet_api.delete_pet(pet_id=pet_body["id"])

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, "Не верный статус ответа: {response.text}"

        with allure.step("Проверка правильности сообщения в ответе"):
            assert response.text == 'Pet deleted', "Не верное сообщение в ответе {response.text}"

        with allure.step("Удаленный питомец не отдается в списке по id"):
            get_response = self.pet_api.get_pet_by_id(pet_id=pet_body["id"])
            assert get_response.status_code == 404, "Не верный статус ответа: {response.text}"

    @allure.title("Удалить питомца по id, которого не существует в системе")
    def test_delete_pet_by_id_does_not_exist(self, create_new_pet):
        with allure.step("Создаем нового питомца и берем его id"):
            pet_id = create_new_pet["id"]

        with allure.step("Удаляем созданного питомца по id"):
            self.pet_api.delete_pet(pet_id=pet_id)

        with allure.step("Совершаем попытку удалить, уже удаленного питомца по id"):
            response = self.pet_api.delete_pet(pet_id=pet_id)

        with allure.step("Проверка статус кода"):
            assert response.status_code == 404, "Не верный статус ответа: {response.text}"

    @allure.title("Загрузка изображения питомца")
    def test_upload_pet_image(self, create_new_pet, temp_image_file):
        pet_body = create_new_pet
        file_path = temp_image_file
        response = self.pet_api.post_upload_pet_image(pet_id=pet_body["id"], file_path=file_path,
                                                      additionalMetadata="test_meta")

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, "Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели Pet"):
            pet_response = Pet.model_validate(response.json())

        with allure.step("Проверка, что файл действительно добавился"):
            assert len(pet_response.photoUrls) == len(pet_body["photoUrls"]) + 1

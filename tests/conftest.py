import os
import tempfile

import pytest
from dotenv import load_dotenv
from src.data_generator.data_generator import generate_pet_body, generate_user_body
from src.petstore_api.pet import PetAPI

load_dotenv()  # Загружаем переменные из .env файла
pet_api = PetAPI()


@pytest.fixture
def generate_body_pet():
    """
    Фикстура создания тела для питомца
    """
    return generate_pet_body


@pytest.fixture()
def create_new_pet(generate_body_pet):
    """
    Фикстура для создание нового питомца и последующим удалением питомца после теста
    """
    pet_body = generate_body_pet(id=True, name=True, photoUrls=True, status=True, tags=True, category=True)
    response = pet_api.post_add_new_pet(body=pet_body).json()
    yield response
    pet_api.delete_pet(pet_id=response["id"])


@pytest.fixture
def delete_pet_after_test():
    """
    Фикстура для удаления питомца после теста.
    """
    pet_id_container = {"id": None}
    yield pet_id_container
    pet_api.delete_pet(pet_id=pet_id_container["id"])


@pytest.fixture
def temp_image_file():
    """
    Фикстура для создания временного файла изображения в тестах.
    Создает временный файл с расширением .jpg, содержащий тестовые данные.
    Файл  удаляется после теста.
    :return:
        str: Абсолютный путь к созданному временному файлу.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(b"test image content")
        tmp.flush()
        file_path = tmp.name

    yield file_path
    os.unlink(file_path)


@pytest.fixture
def generate_body_user():
    """
    Фикстура создания тела запроса для пользователя
    """
    return generate_user_body

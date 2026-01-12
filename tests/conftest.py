import os
import tempfile

import pytest
from dotenv import load_dotenv
from src.data_generator.data_generator import generate_pet_body, generate_user_body, generate_order_body
from src.petstore_api.pet import PetAPI
from src.petstore_api.store import StoreAPI
from src.petstore_api.user import UserAPI

load_dotenv()  # Загружаем переменные из .env файла


@pytest.fixture(scope="session")
def pet_api():
    """
    Фикстура для работы с Pet API.
    Создаёт единственный экземпляр клиента PetAPI на всю сессию запуска тестов,
    что позволяет переиспользовать его во всех тестах без повторной инициализации.
    """
    return PetAPI()


@pytest.fixture(scope="session")
def user_api():
    """
    Фикстура для работы с User API.
    Создаёт единственный экземпляр клиента UserAPI на всю сессию запуска тестов,
    что позволяет переиспользовать его во всех тестах без повторной инициализации.
    """
    return UserAPI()


@pytest.fixture(scope="session")
def store_api():
    """
    Фикстура для работы с Store API.
    Создаёт единственный экземпляр клиента StoreAPI на всю сессию запуска тестов,
    что позволяет переиспользовать его во всех тестах без повторной инициализации.
    """
    return StoreAPI()


@pytest.fixture
def generate_body_pet():
    """
    Фикстура создания тела для питомца
    """
    return generate_pet_body


@pytest.fixture()
def create_new_pet(generate_body_pet, pet_api):
    """
    Фикстура для создание нового питомца и последующим удалением питомца после теста
    """
    pet_body = generate_body_pet(pet_id=True, name=True, photoUrls=True, status=True, tags=True, category=True)
    response = pet_api.post_add_new_pet(body=pet_body).json()
    yield response
    pet_api.delete_pet(pet_id=response["id"])


@pytest.fixture
def delete_pet_after_test(pet_api):
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


@pytest.fixture
def delete_users_after_test(user_api):
    """
    Фикстура для удаления пользователей после теста.
    """
    users_container = []
    yield users_container
    for username in users_container:
        user_api.delete_user(username=username)


@pytest.fixture()
def create_new_user(generate_body_user, user_api):
    """
    Фикстура для создание нового пользователя и последующим удалением пользователя после теста
    """
    user_body = generate_body_user(user_id=True, username=True, first_name=True, last_name=True, email=True,
                                   password=True,
                                   phone=True, user_status=True)
    user_api.post_create_new_user(body=user_body)
    yield user_body
    user_api.delete_user(username=user_body["username"])


@pytest.fixture()
def authorized_user(create_new_user, user_api):
    """
    Фикстура авторизации под пользователем
    """
    username = create_new_user["username"]
    user_password = create_new_user["password"]
    user_api.get_user_login(username=username, password=user_password)
    return username


@pytest.fixture
def generate_body_order():
    """
    Фикстура создания тела запроса для заказа животного
    """
    return generate_order_body


@pytest.fixture
def delete_order_after_test(store_api):
    """
    Фикстура для удаления заказа после теста.
    """
    order_id_container = {"id": None}
    yield order_id_container
    store_api.delete_order(order_id=order_id_container["id"])


@pytest.fixture()
def create_new_order(generate_body_order, create_new_pet, authorized_user, store_api):
    """
    Фикстура для создание нового заказа животного и последующим удалением заказа после теста
    """
    order_body = generate_body_order(order_id=True, quantity=True, ship_date=True, status=True, complete=True)
    order_body['petId'] = create_new_pet['id']
    store_api.post_add_new_order(body=order_body)
    yield order_body
    store_api.delete_order(order_id=order_body['id'])
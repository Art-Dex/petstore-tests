import allure
import pytest

from src.data_generator.data_generator import generate_randon_name
from src.models.user import User, FieldUsernameNotFound
from src.models.api_response import ApiResponse


@allure.epic("Petstore")
@allure.feature("User")
class TestsUser:

    @allure.title("Создание нового пользователя с заполнением всех полей")
    def test_post_create_user_all_fields(self, generate_body_user, delete_users_after_test, user_api):
        user_body = generate_body_user(user_id=True, username=True, first_name=True, last_name=True,
                                       email=True, password=True, phone=True, user_status=True)
        response = user_api.post_create_new_user(body=user_body)

        with allure.step("Успешный статус код ответа"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели ApiResponse"):
            response = ApiResponse.model_validate(response.json())
            assert response.message == str(user_body["id"])

        with allure.step("Проверить, что пользователь действительно создался с переданным данными"):
            create_user_body = user_api.get_user_by_username(user_body["username"]).json()
            assert create_user_body["id"] == user_body["id"]
            assert create_user_body["username"] == user_body["username"]
            assert create_user_body["firstName"] == user_body["firstName"]
            assert create_user_body["lastName"] == user_body["lastName"]
            assert create_user_body["email"] == user_body["email"]
            assert create_user_body["password"] == user_body["password"]
            assert create_user_body["phone"] == user_body["phone"]
            assert create_user_body["userStatus"] == user_body["userStatus"]

        delete_users_after_test.append(user_body["username"])

    @allure.title("Создание нового пользователя с заполнением только  имени и пароля")
    def test_post_create_user_by_filling_only_username_and_password(self, generate_body_user, delete_users_after_test,
                                                                    user_api):
        user_body = generate_body_user(username=True, password=True)
        response = user_api.post_create_new_user(body=user_body)

        with allure.step("Успешный статус код ответа"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели ApiResponse"):
            ApiResponse.model_validate(response.json())

        with allure.step("Проверить, что пользователь действительно создался с переданным данными"):
            create_user_body = user_api.get_user_by_username(user_body["username"]).json()
            assert create_user_body["username"] == user_body["username"]
            assert create_user_body["password"] == user_body["password"]

        delete_users_after_test.append(user_body["username"])

    @allure.title("Создание нового пользователя c пустым телом запроса")
    def test_post_create_user_with_an_empty_request_body(self, user_api):
        response = user_api.post_create_new_user(body={})

        with allure.step("Статус код ответа с ошибкой на клиенте"):
            assert response.status_code in (400, 409, 411, 415, 422), f"Не верный статус ответа: {response.text}"

    @pytest.mark.parametrize("users_count", [1, 2, 3])
    @allure.title("Создание новых пользователей списком в количестве {users_count} с заполнением всех полей")
    def test_post_create_users_with_list_all_fields(self, generate_body_user, delete_users_after_test,
                                                    users_count, user_api):
        users_body = [generate_body_user(user_id=True, username=True, first_name=True, last_name=True, email=True,
                                         password=True, phone=True, user_status=True) for _ in range(users_count)]

        response = user_api.post_create_new_users_with_list(body=users_body)

        with allure.step("Успешный статус код ответа"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели ApiResponse"):
            response = ApiResponse.model_validate(response.json())
            assert response.message == "ok"

        with allure.step("Проверить, что пользователи действительно создались с переданными данными"):
            for user in users_body:
                create_user_body = user_api.get_user_by_username(user["username"]).json()
                assert create_user_body["id"] == user["id"]
                assert create_user_body["username"] == user["username"]
                assert create_user_body["firstName"] == user["firstName"]
                assert create_user_body["lastName"] == user["lastName"]
                assert create_user_body["email"] == user["email"]
                assert create_user_body["password"] == user["password"]
                assert create_user_body["phone"] == user["phone"]
                assert create_user_body["userStatus"] == user["userStatus"]

        for user in users_body:
            delete_users_after_test.append(user["username"])

    @pytest.mark.parametrize("users_count", [2])
    @allure.title("Создание пользователей списком в количестве {users_count} заполнением только  имени и пароля")
    def test_post_create_users_with_list_by_filling_only_username_and_password(self,
                                                                               generate_body_user,
                                                                               delete_users_after_test,
                                                                               users_count,
                                                                               user_api):
        users_body = [generate_body_user(username=True, password=True) for _ in range(users_count)]

        response = user_api.post_create_new_users_with_list(body=users_body)

        with allure.step("Успешный статус код ответа"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели ApiResponse"):
            response = ApiResponse.model_validate(response.json())
            assert response.message == "ok"

        with allure.step("Проверить, что пользователи действительно создались с переданными данными"):
            for user in users_body:
                create_user_body = user_api.get_user_by_username(user["username"]).json()
                assert create_user_body["username"] == user["username"]
                assert create_user_body["password"] == user["password"]

        for user in users_body:
            delete_users_after_test.append(user["username"])

    @allure.title("Получить информацию о пользователе по username")
    def test_get_user_by_username(self, create_new_user, user_api):
        user_body = create_new_user
        response = user_api.get_user_by_username(username=user_body["username"])

        with allure.step("Успешный статус код ответа"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели User"):
            user_response = User.model_validate(response.json())

        with allure.step("В ответе содержится информация о том пользователе, чей username передавался в запросе"):
            assert user_response.id == user_body["id"]
            assert user_response.username == user_body["username"]

    @allure.title("Отправить запрос на получение иформации о пользователе с несуществующим username")
    def test_get_user_by_with_a_non_existent_username(self, user_api):
        username = generate_randon_name()
        response = user_api.get_user_by_username(username=username)

        with allure.step("Статус код с ошибкой 404"):
            assert response.status_code == 404, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели FieldUsernameNotFound"):
            actual = FieldUsernameNotFound.model_validate(response.json())

        with allure.step("Ответ содержит ожидаемые значения"):
            expected = FieldUsernameNotFound()
            assert actual == expected

    @allure.title("Изменение всех полей в данных о пользователи, кроме имени")
    def test_put_update_user_all_fields_except_name(self, generate_body_user, create_new_user, user_api):
        username = create_new_user["username"]
        user_body = generate_body_user(user_id=True, first_name=True, last_name=True,
                                       email=True, password=True, phone=True, user_status=True)
        response = user_api.put_updates_user(username=username, body=user_body)

        with allure.step("Успешный статус код ответа"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели ApiResponse"):
            response = ApiResponse.model_validate(response.json())
            assert response.message == str(user_body["id"])

        with allure.step("Проверить, что у пользователя изменились все передаваемые параметры"):
            update_user_body = user_api.get_user_by_username(username).json()
            assert update_user_body["id"] == user_body["id"], 'Параметр не изменился'
            assert update_user_body["firstName"] == user_body["firstName"], 'Параметр не изменился'
            assert update_user_body["lastName"] == user_body["lastName"], 'Параметр не изменился'
            assert update_user_body["email"] == user_body["email"], 'Параметр не изменился'
            assert update_user_body["password"] == user_body["password"], 'Параметр не изменился'
            assert update_user_body["phone"] == user_body["phone"], 'Параметр не изменился'
            assert update_user_body["userStatus"] == user_body["userStatus"], 'Параметр не изменился'

    @pytest.mark.parametrize(
        "missing, body_kwargs",
        [
            (
                    "id",
                    dict(user_id=True)
            ),
            (
                    "firstName",
                    dict(first_name=True)
            ),
            (
                    "lastName",
                    dict(last_name=True)
            ),
            (
                    "email",
                    dict(email=True)
            ),
            (
                    "password",
                    dict(password=True)
            ),
            (
                    "phone",
                    dict(phone=True)
            ),
            (
                    "userStatus",
                    dict(user_status=True)
            ),
        ]
    )
    @allure.title("Изменить одно поле {missing} в данных о пользователи")
    def test_put_update_user_one_field(self, generate_body_user, create_new_user, missing, body_kwargs, user_api):
        user = create_new_user
        user_body = generate_body_user(**body_kwargs)
        response = user_api.put_updates_user(username=user["username"], body=user_body)

        with allure.step("Успешный статус код ответа"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели ApiResponse"):
            ApiResponse.model_validate(response.json())

        with allure.step("Проверить, что у пользователя изменилися передаваемый параметр"):
            update_user_body = user_api.get_user_by_username(user["username"]).json()
            assert update_user_body[missing] != user[missing], 'Параметр не изменился'
            assert update_user_body[missing] == user_body[missing], 'Параметр не изменился'

    @allure.title("Изменить username в данных о пользователи")
    def test_put_update_username(self, generate_body_user, create_new_user, user_api):
        user = create_new_user
        user_body = generate_body_user(username=True)
        response = user_api.put_updates_user(username=user["username"], body=user_body)

        with allure.step("Успешный статус код ответа"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели ApiResponse"):
            ApiResponse.model_validate(response.json())

        with allure.step("Проверить, что у пользователя изменилися  username"):
            update_user_body = user_api.get_user_by_username(user_body["username"]).json()
            assert update_user_body["username"] != user["username"], 'Параметр не изменился'
            assert update_user_body["username"] == user_body["username"], 'Параметр не изменился'

        with allure.step("Проверить, что не существует пользователя со старым username"):
            old_user = user_api.get_user_by_username(user["username"])
            assert old_user.status_code == 404, f"Не верный статус ответа: {response.text}"

    @allure.title("Удалить пользователя")
    def test_delete_user_by_username(self, create_new_user, user_api):
        username = create_new_user["username"]
        response = user_api.delete_user(username=username)

        with allure.step("Успешный статус код ответа"):
            assert response.status_code == 200, "Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели ApiResponse"):
            ApiResponse.model_validate(response.json())

        with allure.step("Удаленный пользователь не отдается в списке по username"):
            get_response = user_api.get_user_by_username(username)
            assert get_response.status_code == 404, f"Не верный статус ответа: {response.text}"

    @allure.title("Удалить пользователя, которого не существует в системе")
    def test_delete_user_by_username_does_not_exist(self, user_api):
        username = generate_randon_name()
        with allure.step("Удаляем пользователя по несуществующему в системе имени"):
            response = user_api.delete_user(username=username)

        with allure.step("Статус код с ошибкой 404"):
            assert response.status_code == 404, f"Не верный статус ответа: {response.text}"

    @allure.title("Авторизоваться под пользователем по валидному логину и паролю")
    def test_get_login_user_valid_login_and_password(self, create_new_user, user_api):
        user_body = create_new_user

        with allure.step("Авторизоваться под пользователем, указав верный username и пароль"):
            response = user_api.get_user_login(username=user_body["username"], password=user_body["password"])

        with allure.step("Успешный статус код ответа"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели ApiResponse"):
            ApiResponse.model_validate(response.json())

    @allure.title("Авторизоваться под пользователем, указав невалидный username")
    def test_get_login_user_invalid_username(self, create_new_user, user_api):
        username = generate_randon_name()
        user_password = create_new_user["password"]

        with allure.step("Осуществить попытку авторизации"):
            response = user_api.get_user_login(username=username, password=user_password)

        with allure.step("Статус код с ошибкой 400"):
            assert response.status_code == 400, f"Не верный статус ответа: {response.text}"

    @allure.title("Авторизоваться под пользователем, указав невалидный пароль")
    def test_get_login_user_invalid_password(self, create_new_user, user_api):
        username = create_new_user["username"]
        user_password = generate_randon_name()

        with allure.step("Осуществить попытку авторизации"):
            response = user_api.get_user_login(username=username, password=user_password)

        with allure.step("Статус код с ошибкой 400"):
            assert response.status_code == 400, f"Не верный статус ответа: {response.text}"

    @allure.title("Разлогинится под авторизованным пользователем")
    def test_get_logout_authorized_user(self, authorized_user, user_api):
        with allure.step("Разлогинится под пользователем"):
            response = user_api.get_user_logout()

        with allure.step("Успешный статус код ответа"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели ApiResponse"):
            ApiResponse.model_validate(response.json())
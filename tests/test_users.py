import allure

from src.models.user import User
from src.petstore_api.user import UserAPI


@allure.epic("Petstore")
@allure.feature("User")
class TestsUser:
    user_api = UserAPI()

    @allure.title("Создание нового пользователя с заполнением всех полей")
    def test_post_create_user_all_fields(self, generate_body_user):
        user_body = generate_body_user(id=True, username=True, first_name=True, last_name=True,
                                       email=True, password=True, phone=True, user_status=True)
        response = self.user_api.post_create_new_user(body=user_body)

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, f"Не верный статус ответа: {response.text}"

        with allure.step("Ответ соответствует модели User"):
            user_response = User.model_validate(response.json())

        with allure.step("Сверка отправленных данных с полученными"):
            assert user_response.id == user_body["id"]
            assert user_response.username == user_body["name"]
            assert user_response.firstName == user_body["firstName"]
            assert user_response.lastName == user_body["lastName"]
            assert user_response.email == user_body["email"]
            assert user_response.password == user_body["password"]
            assert user_response.phone == user_body["phone"]
            assert user_response.userStatus == user_body["userStatus"]

import allure


@allure.epic("Petstore")
@allure.feature("E2E Petstore")
class TestPetstoreE2E:

    @allure.title("Создание пользователя → логин → заказ животного")
    def test_create_user_login_and_order(self,
                                         generate_body_user,
                                         delete_users_after_test,
                                         generate_body_order,
                                         delete_order_after_test,
                                         create_new_pet,
                                         user_api,
                                         store_api):
        with allure.step("Создать нового пользователя с заполнением всех полей"):
            user_body = generate_body_user(user_id=True, username=True, first_name=True, last_name=True,
                                           email=True, password=True, phone=True, user_status=True)
            response_create_user = user_api.post_create_new_user(body=user_body)

        with allure.step("Успешный статус код на запрос создания пользователя"):
            assert response_create_user.status_code == 200, f"Не верный статус ответа: {response_create_user.text}"

        with allure.step("Проверить, что пользователь действительно создался с переданным данными"):
            create_user_body = user_api.get_user_by_username(user_body["username"]).json()
            assert create_user_body["id"] == user_body["id"]
            assert create_user_body["username"] == user_body["username"]
            assert create_user_body["password"] == user_body["password"]

        with allure.step("Авторизоваться под созданым пользователем"):
            response_auth = user_api.get_user_login(username=create_user_body["username"],
                                                    password=create_user_body["password"])

        with allure.step("Успешный статус код на запрос авторизации пользователя"):
            assert response_auth.status_code == 200, f"Не верный статус ответа: {response_auth.text}"

        with allure.step("Оформить заказ на животного"):
            order_body = generate_body_order(order_id=True, quantity=True, ship_date=True, status=True, complete=True)
            order_body['petId'] = create_new_pet['id']
            response_add_order = store_api.post_add_new_order(body=order_body)

        with allure.step("Успешный статус код на запрос на добавление заказа"):
            assert response_add_order.status_code == 200, f"Не верный статус ответа: {response_add_order.text}"

        with allure.step("Проверить, что заказ действительно создался с переданным данными"):
            order_response_body = response_add_order.json()
            assert order_response_body["id"] == order_body["id"]
            assert order_response_body["petId"] == order_body["petId"]

        delete_order_after_test['id'] = order_body["id"]
        delete_users_after_test.append(user_body["username"])

    @allure.title("Создание питомца → обновление животного → заказ")
    def test_create_update_and_order_pet(self,
                                         authorized_user,
                                         generate_body_pet,
                                         generate_body_order,
                                         delete_pet_after_test,
                                         delete_order_after_test,
                                         pet_api,
                                         store_api):
        with allure.step("Создать нового питомца с заполнением всех полей"):
            pet_body_1 = generate_body_pet(pet_id=True, name=True, photoUrls=True, status=True, tags=True,
                                           category=True)
            response_pet = pet_api.post_add_new_pet(body=pet_body_1)

        with allure.step("Успешный статус код на запрос создания питомца"):
            assert response_pet.status_code == 200, f"Не верный статус ответа: {response_pet.text}"

        with allure.step("Проверить, что питомец действительно создался с переданным данными"):
            response_pet_body_1 = response_pet.json()
            assert response_pet_body_1["id"] == pet_body_1["id"]
            assert response_pet_body_1["name"] == pet_body_1["name"]

        with allure.step("Изменить все поля в данных о питомце"):
            pet_body_2 = generate_body_pet(name=True, photoUrls=True, status=True, tags=True, category=True)
            pet_body_2['id'] = response_pet_body_1['id']
            response_update_pet = pet_api.put_update_pet(body=pet_body_2)

        with allure.step("Успешный статус код на запрос обновления питомца"):
            assert response_update_pet.status_code == 200, f"Не верный статус ответа: {response_pet.text}"

        with allure.step("Сверка отправленных данных с полученными"):
            response_update_pet_body = response_update_pet.json()
            assert response_update_pet_body["id"] == response_pet_body_1["id"]
            assert response_update_pet_body["name"] == pet_body_2["name"]
            assert response_update_pet_body["photoUrls"] == pet_body_2["photoUrls"]
            assert response_update_pet_body["status"] == pet_body_2["status"]
            assert response_update_pet_body["tags"][0] == pet_body_2["tags"][0]
            assert response_update_pet_body["category"] == pet_body_2["category"]

        with allure.step("Оформить заказ на животного"):
            order_body = generate_body_order(order_id=True, quantity=True, ship_date=True, status=True, complete=True)
            order_body['petId'] = response_update_pet_body['id']
            response_add_order = store_api.post_add_new_order(body=order_body)

        with allure.step("Успешный статус код на запрос на добавление заказа"):
            assert response_add_order.status_code == 200, f"Не верный статус ответа: {response_add_order.text}"

        with allure.step("Проверить, что заказ действительно создался с переданным данными"):
            order_response_body = response_add_order.json()
            assert order_response_body["id"] == order_body["id"]
            assert order_response_body["petId"] == order_body["petId"]

        delete_order_after_test["id"] = order_response_body["id"]
        delete_pet_after_test["id"] = response_update_pet_body["id"]

    @allure.title("Логин → заказ → удаление заказа")
    def test_login_order_and_delete(self,
                                    create_new_user,
                                    create_new_pet,
                                    generate_body_order,
                                    user_api,
                                    store_api):
        with allure.step("Авторизоваться под  пользователем"):
            create_user_body = create_new_user
            response_auth = user_api.get_user_login(username=create_user_body["username"],
                                                    password=create_user_body["password"])

        with allure.step("Успешный статус код на запрос авторизации пользователя"):
            assert response_auth.status_code == 200, f"Не верный статус ответа: {response_auth.text}"

        with allure.step("Оформить заказ на животного"):
            order_body = generate_body_order(order_id=True, quantity=True, ship_date=True, status=True, complete=True)
            order_body['petId'] = create_new_pet['id']
            response_add_order = store_api.post_add_new_order(body=order_body)

        with allure.step("Успешный статус код на запрос на добавление заказа"):
            assert response_add_order.status_code == 200, f"Не верный статус ответа: {response_add_order.text}"

        with allure.step("Проверить, что заказ действительно создался с переданным данными"):
            order_response_body = response_add_order.json()
            assert order_response_body["id"] == order_body["id"]
            assert order_response_body["petId"] == order_body["petId"]

        with allure.step("Удалить созданный заказ"):
            response_delete_order = store_api.delete_order(order_id=order_response_body["id"])

        with allure.step("Успешный статус код на запрос удаления заказа"):
            assert response_delete_order.status_code == 200, f"Не верный статус ответа: {response_delete_order.text}"

        with (allure.step("Проверить, что удаленный заказ не отдается по id")):
            response_get_order_by_id = store_api.get_order_by_id(order_id=order_response_body["id"])
            assert response_get_order_by_id.status_code == 404, f"Не верный статус ответа: {response_get_order_by_id.text}"
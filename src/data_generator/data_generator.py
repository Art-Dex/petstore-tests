import random
from faker import Faker
from datetime import timezone

faker = Faker('en_US')


def generate_randon_name():
    """
    Генерация рандомного имени
    :return: str
    """
    return "test-" + faker.first_name() + "-" + str(random.randint(1, 999))


def generate_randon_status_pet():
    """
    Генерация рандомного статуса животного
    :return: str
    """
    return random.choice(["available", "pending", "sold"])


def generate_pet_body(pet_id=False, name=False, photoUrls=False, status=False, tags=False, category=False) -> dict:
    """
   #           Генерация тела запроса питомца с опциональной генерацией полей.
   #           Если поле передано со значением True, оно будет сгенерировано,
   #           остальные поля остаются пустыми.
   #           """
    body = {
    }

    if pet_id:
        body["id"] = random.randint(10000, 99999)
    if name:
        body["name"] = "test-pet-" + faker.first_name()
    if photoUrls:
        body["photoUrls"] = [faker.url()]
    if status:
        body["status"] = generate_randon_status_pet()
    if tags:
        body["tags"] = [{
            "id": random.randint(10000, 99999),
            "name": faker.first_name()
        }]
    if category:
        body["category"] = {
            "id": random.randint(10000, 99999),
            "name": faker.first_name()
        }

    return body


def generate_user_body(user_id=False, username=False, first_name=False, last_name=False,
                       email=False, password=False, phone=False, user_status=False) -> dict:
    """
   #           Генерация тела запроса пользователя с опциональной генерацией полей.
   #           Если поле передано со значением True, оно будет сгенерировано,
   #           остальные поля остаются пустыми.
   #           """
    body = {
    }

    name = faker.first_name()
    if user_id:
        body["id"] = random.randint(10000, 99999)
    if username:
        body["username"] = "test-user-" + name + str(random.randint(1, 999))
    if first_name:
        body["firstName"] = name
    if last_name:
        body["lastName"] = faker.last_name()
    if email:
        body["email"] = faker.email()
    if password:
        body["password"] = faker.password()
    if phone:
        body["phone"] = faker.phone_number()
    if user_status:
        body["userStatus"] = random.randint(1, 999)

    return body


def generate_randon_status_order():
    """
    Генерация рандомного статуса заказа
    :return: str
    """
    return random.choice(["placed", "approved", "delivered"])


def generate_datetime() -> str:
    """
    Генерирует дату в формате:
    2025-12-24T06:56:38.018+0000
    """
    dt = faker.date_time(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+0000"


def generate_order_body(order_id=False, pet_id=False, quantity=False, ship_date=False, status=False,
                        complete=False) -> dict:
    """
   #           Генерация тела запроса заказа на питомца с опциональной генерацией полей.
   #           Если поле передано со значением True, оно будет сгенерировано,
   #           остальные поля остаются пустыми.
   #           """
    body = {
    }

    if order_id:
        body["id"] = random.randint(10000, 99999)
    if pet_id:
        body["petId"] = random.randint(10000, 99999)
    if quantity:
        body["quantity"] = random.randint(1, 100)
    if ship_date:
        body["shipDate"] = generate_datetime()
    if status:
        body["status"] = generate_randon_status_order()
    if complete:
        body["complete"] = random.choice([True, False])

    return body

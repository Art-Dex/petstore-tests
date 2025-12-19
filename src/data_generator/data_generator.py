import random
from faker import Faker

faker = Faker('en_US')


def generate_randon_name():
    """
    Генерация рандомного имени
    :return: str
    """
    return "test-pet-" + faker.first_name()


def generate_randon_status_pet():
    """
    Генерация рандомного статуса животного
    :return: str
    """
    return random.choice(["available", "pending", "sold"])


def generate_pet_body(id=False, name=False, photoUrls=False, status=False, tags=False, category=False) -> dict:
    """
   #           Генерация тела запроса питомца с опциональной генерацией полей.
   #           Если поле передано со значением True, оно будет сгенерировано,
   #           остальные поля остаются пустыми.
   #           """
    body = {
    }

    if id:
        body["id"] = random.randint(10000, 99999)
    if name:
        body["name"] = "test-pet-" + faker.first_name()
    if photoUrls:
        body["photoUrls"] = [faker.url()]
    if status:
        body["status"] = random.choice(["available", "pending", "sold"])
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


def generate_user_body(id=False, username=False, first_name=False, last_name=False,
                       email=False, password=False, phone=False, user_status=False) -> dict:
    """
   #           Генерация тела запроса пользователя с опциональной генерацией полей.
   #           Если поле передано со значением True, оно будет сгенерировано,
   #           остальные поля остаются пустыми.
   #           """
    body = {
    }

    name = faker.first_name()
    if id:
        body["id"] = random.randint(10000, 99999)
    if username:
        body["name"] = "test-user-" + name
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

# Petstore API Autotests

Автоматизированный тестовый проект для Swagger Petstore API  
https://petstore3.swagger.io/

Проект реализован на **Python + Pytest + Requests**, с использованием:
- Allure для отчётности
- Pydantic для валидации контрактов
- Docker для воспроизводимой среды
- GitLab CI для CI/CD

---

##  Цель проекта

- Покрыть REST API автотестами
- Проверять позитивные и негативные сценарии
- Валидировать ответы по документации API

---

## Стек технологий

- Python 3.11
- Pytest
- Requests
- Pydantic v2
- Allure
- Docker
- GitLab CI

---

##  Структура проекта 

```
petstore-api-tests/

├── src/
│ ├── http_client/ # HTTP клиент
│ ├── petstore_api/ # API-обёртки (Pet, Store, User)
│ ├── models/ # Pydantic модели
│ ├── data_generator/ # Генераторы тестовых данных
│
├── tests/
│ ├── test_pet.py
│ ├── test_store.py
│ ├── test_user.py
│ └── conftest.py
│
├── .github/
│ ├── workflows/
│
├── Dockerfile
├── requirements.txt
├── pytest.ini
├── env.example
└── README.md
```
___
##  Конфигурация окружения
Проект использует переменные окружения для конфигурации.
В корне репозитория находится файл `env.example`, содержащий список необходимых переменных окружения и пример их значений.

### Настройка локального окружения
1. Создайте в корне проекта файл `.env`
2. Скопируйте в созданный файл содержимое из `env.example`
3. Укажети необходимые значения в переменные окружения в файле `.env`

Переменные окружения загружаются из `.env` файла с помощью библиотеки `python-dotenv`.

⚠️ Файл `.env` не должен коммититься в репозиторий и добавлен в .gitignore


___
## Запуск тестов локально
### 1. Установить зависимости

```bash
pip install -r requirements.txt
```
### 2. Запустить тесты
```bash
pytest
```

### 3. Запуск с Allure
```bash
pytest --alluredir=allure-results
allure serve allure-results
```
___
## Запуск через Docker

### Сборка образа
```bash
docker build -t petstore-tests .
```

### Запуск тестов
```bash
docker run --rm petstore-tests
```
### Запуск с сохранением Allure результатов
```bash
docker run --rm -v ${PWD}/allure-results:/app/allure-results petstore-tests
```
___
## Allure отчёты
В отчётах отображаются:
- шаги тестов
- HTTP-запросы и ответы
- валидация моделей API
- причины падения тестов

___

## CI/CD
Проект использует  GitHub Actions:
- сборка Docker-образа
- запуск тестов внутри контейнера
- сохранение Allure результатов как artifacts
- pipeline запускается вручную в разделе GitHub → Actions -> API tests in Docker with Allure

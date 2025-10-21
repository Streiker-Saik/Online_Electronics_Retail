# Онлайн платформа_торговой сети электроники

## Содержание:
- [Описание](#описание)
- [Установка](#установка)
- [Запуск проекта](#запуск-проекта)
- [Запуск тестов](#запуск-тестов)
- [Кастомные команды](#кастомные-команды)
- [Структура проекта](#структура-проекта)
- [Приложение electro](#приложение-electro)
  - [Admin electro](#admin-electro)
  - [Models electro](#models-electro)
    - [Contact](#contact)
    - [Product](#product)
  - [Permissions electro](#permissions-electro)
  - [Serializers electro](#serializers-electro)
    - [ContactSerializer](#contactserializer)
    - [ProductSerializer](#productserializer)
  - [Urls electro](#urls-electro)
  - [Views electro](#views-electro)
    - [ContactViewSet](#contactviewset)
    - [ProductViewSet](#productviewset)

## Описание:

Веб-приложение с API-интерфейсом и админ-панелью.
С базой данных и Django.
Стек: Python, Django, DRF, PostgreSQL

[<- на начало](#содержание)

---
## Установка:
- Проверить версию Python:  
    Убедитесь, что у вас установлен Python (версия 3.8+). Вы можете проверить установленную версию Python, выполнив команду:
    ```
    python --version
    ```
- Клонируйте репозиторий:
    ```bash
    git clone git@github.com:Streiker-Saik/Online_Electronics_Retail.git
    ```
- Перейдите в директорию проекта:
    ```
    cd Online_Electronics_Retail
    ```
- ### При использовании PIP:
  - Активируйте виртуальное окружение
    ```
    python -m venv <имя_вашего окружения>
    <имя_вашего_окружения>\Scripts\activate
    ```
  - Установите зависимости
    ```
    pip install -r requirements.txt
    ```
- ### При использование POETRY:
  - Если у вас еще не установлен Poetry, вы можете установить его, выполнив следующую команду
      ```bash
      curl -sSL https://install.python-poetry.org | python3 -
      ```
  - Проверить Poetry добавлен в ваш PATH.
      ```bash
      poetry --version
      ```
  - Активируйте виртуальное окружение
      ```bash
      poetry shell
      ```
  - Установите необходимые зависимости:
      ```bash
      poetry install
      ```

- ### Зайдите в файл .env.example и следуйте инструкция

[<- на начало](#содержание)

---
## Запуск проекта:
### Локально:
- Чтобы запустить сервер разработки, выполните следующую команду:
  ```bash
  python manage.py runserver
  ```

[<- на начало](#содержание)

---
## Тестирование:
- Запустить тесты 
  ```bash
  python manage.py test
  ```
- Запустить с покрытием тесты
  ```bash
  coverage run --source='.' manage.py test
  ```
    - Записать/обновить в файл html
    ```bash
    coverage html
    ```
    - Вывести в терминал
    ```bash
    coverage report
    ```

[<- на начало](#содержание)

---
## Кастомные команды
### csu
Команда для создания суперпользователя по ключам: username, password.
- Если не указано, то: username='admin', password='admin'.
  ```bash
  python manage.py csu
  ```
- Возможно указать свои данные:
  ```
  python manage.py csu --username ввести_логин --password ввести_пароль
  ```

[<- на начало](#содержание)

---
## Структура проекта:
```
Online_Electronics_Retail/
├── config/
|   ├── __init__.py
|   ├── asgi.py
|   ├── settings.py # настройки проекта
|   ├── urls.py # маршрутизация проета
|   └── wsgi.py
├── electro/ # приложение сети поставщиков продуктов
|   ├── management/
|   |   └── commands/ # кастомные команды
|   |   |   └── csu # создание суперпользователя
|   ├── migrations/ # пакет миграции моделей
|   |   └── ...
|   ├── tests/ # пакет тестов
|   |   ├── __init__.py
|   |   ├── test_contacts.py # тесты контактов
|   |   └── test_products.py # тесты продуктов
|   ├── admin.py 
|   ├── apps.py
|   ├── models.py # модели БД
|   ├── permissions.py # права доступа
|   ├── serializaters.py # сериализаторы
|   ├── tests.py 
|   ├── urls.py # маршрутизация приложения
|   └── views.py # конструктор контроллеров
├── .env
├── .flake8 # настройка для flake8
├── .gitignore
├── poetry.lock
├── pypproject.toml # зависимости для poetry
├── README.md
└── requirements.txt # зависимости для pip
```

[<- на начало](#содержание)

---
# Приложение electro:
## Admin electro:
### ContactAdmin:
Класс для работы администратора с контактами
- Атрибуты:
  - ordering - сортировка по email
  - list_filter - фильтрация: страна, город
  - list_display - выводит на экран: email, страна, город
  - search_fields - поиск по: email, страна, город
### ProductAdmin:
Класс для работы администратора с продуктами
- Атрибуты:
  - ordering - сортировка по дате выхода на рынок
  - list_display - выводит на экран: название, модель, дата выхода на рынок
  - search_fields - поиск по: название, модель

[<- на начало](#содержание)

---
## Models electro
### Contact:
Представление контактной информации
- Атрибуты:
  - email(EmailField): Электронная почта
  - country(str): Страна
  - city(str): Город
  - street(str): Улица
  - house_number(str): Номер дома
### Product:
Представление продуктов
- Атрибуты:
  - name(str): Название
  - model(str): Модель
  - release_date(datetime): Дата выхода на рынок

[<- на начало](#содержание)

---
## Permissions electro:
### IsActiveUser:
Право активного пользователя

[<- на начало](#содержание)

---
## Serializers electro:
### ContactSerializer:
Сериализатор для модели Contact
- Отображаются поля:
  - id(int): Уникальный идентификатор контакта.
  - email(str): Email.
  - country(str): Страна.
  - city(str): Город.
  - street(str): Улица.
  - house_number(str): Номер дома.
### ProductSerializer:
Сериализатор для модели Product
- Отображаются поля:
  - id(int): Уникальный идентификатор продукта.
  - name(str): Название.
  - model(str): Модель.
  - release_date(datetime): Дата выхода на рынок.

[<- на начало](#содержание)

---

## Urls electro:
- Список и добавление контакта(-ов) (методы: **GET/POST**)  
  http://127.0.0.1:8000/contacts/
- Получение/изменение/удаление контакта (методы: **GET/PUT/PATH/DELETE**)  
  http://127.0.0.1:8000/contacts/(pk)/
  - где (pk) - это, целое число PrimaryKey, ID контакта
- Список и добавление продукта(-ов) (методы: **GET/POST**)  
  http://127.0.0.1:8000/products/
- Получение/изменение/удаление продукта (методы: **GET/PUT/PATH/DELETE**)  
  http://127.0.0.1:8000/products/(pk)/
  - где (pk) - это, целое число PrimaryKey, ID продукта

[<- на начало](#содержание)

---
## Views electro:
### ContactViewSet:
Представление набора действий для модели Contact.  
Позволяет выполнять операции с контактами:
- отображение списка, создание, отображение, полное обновление, частичное обновление, удаление.
### ProductViewSet:
Представление набора действий для модели Product.  
Позволяет выполнять операции с контактами:
- отображение списка, создание, отображение, полное обновление, частичное обновление, удаление.

[<- на начало](#содержание)

---
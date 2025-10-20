# Онлайн платформа_торговой сети электроники

## Содержание:
- [Описание](#описание)
- [Установка](#установка)
- [Запуск проекта](#запуск-проекта)
- [Запуск тестов](#запуск-тестов)
- [Кастомные команды](#кастомные-команды)
- [Структура проекта](#структура-проекта)
- [Приложение electro](#приложение-electro)
  - [Models electro](#models-electro)
    - [Contact](#contact)
  - [Permissions electro](#permissions-electro)
  - [Serializers electro](#serializers-electro)
  - [Urls electro](#urls-electro)
  - [Views electro](#views-electro)
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
## Запуск тестов:
pass

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

[<- на начало](#содержание)

---
## Permissions electro:
### IsActiveUser:
Право авторизованного и активного пользователя

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

[<- на начало](#содержание)

---

## Urls electro:
- Список и добавление контакта(-ов) (методы: **GET/POST**)  
  http://127.0.0.1:8000/contact/
- Получение/изменение/удаление контакта (методы: **GET/PUT/PATH/DELETE**)  
  http://127.0.0.1:8000/contact/(pk)/
  - где (pk) - это, целое число PrimaryKey, ID контакта

[<- на начало](#содержание)

---
## Views electro:
### ContactViewSet:
Представление набора действий для модели Contact.  
Позволяет выполнять операции с контактами:
- отображение списка, создание, отображение, полное обновление, частичное обновление, удаление.

[<- на начало](#содержание)

---
from rest_framework import serializers

from electro.models import Contact, Network, Product


class ContactSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Contact
    Отображаются поля:
        id(int): Уникальный идентификатор контакта.
        email(str): Email.
        country(str): Страна.
        city(str): Город.
        street(str): Улица.
        house_number(str): Номер дома.
    """

    class Meta:
        model = Contact
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product
    Отображаются поля:
        id(int): Уникальный идентификатор продукта.
        name(str): Название.
        model(str): Модель.
        release_date(datetime): Дата выхода на рынок.
    """

    class Meta:
        model = Product
        fields = "__all__"


class NetworkSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Network
    Отображаются поля:
        id(int): Уникальный идентификатор звена сети.
        name(str): Название.
        contacts (ForeignKey): ID контактов
        products (ManyToManyField): Список id продуктов
        supplier (ForeignKey): ID поставщика
        debt (Decimal): Задолженность перед поставщиком
        level (int): Уровень звена в иерархии (0, 1, 2)
        created_at (datetime): Дата и время создания
    """

    class Meta:
        model = Network
        fields = "__all__"


class NetworkListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка моделей Network
    Отображаются поля:
        id(int): Уникальный идентификатор звена сети.
        name(str): Название.
        contacts (ForeignKey): Контактная информация
            id(int): Уникальный идентификатор контакта.
            email(str): Email.
            country(str): Страна.
            city(str): Город.
            street(str): Улица.
            house_number(str): Номер дома.
        products (ManyToManyField): Список продуктов
            id(int): Уникальный идентификатор продукта.
            name(str): Название.
            model(str): Модель.
            release_date(datetime): Дата выхода на рынок.
        supplier (ForeignKey): Поставщик, связанная модель с другим звеном сети
        debt (Decimal): Задолженность перед поставщиком
        level (int): Уровень звена в иерархии (0, 1, 2)
        created_at (datetime): Дата и время создания
    """

    contacts = ContactSerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = Network
        fields = "__all__"


class NetworkUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления модели Network
    Исключены поля:
        debt (float): Задолженность перед поставщиком
    """

    class Meta:
        model = Network
        exclude = ("debt",)

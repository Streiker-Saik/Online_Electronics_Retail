from rest_framework import serializers

from electro.models import Contact, Product


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

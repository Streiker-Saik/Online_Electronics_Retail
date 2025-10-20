from rest_framework import serializers

from electro.models import Contact


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

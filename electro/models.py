from typing import Type

from django.db import models


class Contact(models.Model):
    """
    Представление контактной информации
    Атрибуты:
        email(EmailField): Электронная почта
        country(str): Страна
        city(str): Город
        street(str): Улица
        house_number(str): Номер дома
    """
    objects: Type[models.Manager]

    email = models.EmailField(verbose_name="Электронная почта", help_text="Введите email")
    country = models.CharField(max_length=100, verbose_name="Страна", help_text="Введите страну")
    city = models.CharField(max_length=100, verbose_name="Город", help_text="Введите город")
    street = models.CharField(max_length=100, verbose_name="Улица", help_text="Введите улицу")
    house_number = models.CharField(max_length=10, verbose_name="Номер дома", help_text="Введите номер дома")

    def __str__(self) -> str:
        return f"{self.email}, {self.country}, {self.city}, {self.street}, {self.house_number}"

    class Meta:
        verbose_name = "контакт"
        verbose_name_plural = "контакты"


class Product(models.Model):
    """
    Представление продуктов
    Атрибуты:
        name(str): Название
        model(str): Модель
        release_date(datetime): Дата выхода на рынок
    """
    objects: Type[models.Manager]

    name = models.CharField(max_length=255, verbose_name="Название", help_text="Введите название")
    model = models.CharField(max_length=100, verbose_name="Модель", help_text="Введите модель")
    release_date  = models.DateField(verbose_name="Дата выхода на рынок", help_text="Введите дату выхода на рынок")

    def __str__(self) -> str:
        return f"{self.name} ({self.model})"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"

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

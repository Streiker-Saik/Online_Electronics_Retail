from typing import Type

from django.db import models
from rest_framework.exceptions import ValidationError


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
    release_date = models.DateField(verbose_name="Дата выхода на рынок", help_text="Введите дату выхода на рынок")

    def __str__(self) -> str:
        return f"{self.name} ({self.model})"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"


class Network(models.Model):
    """
    Представление звена сети
    Атрибуты:
        name (str): Название компании
        contacts (ForeignKey): Контактная информация
        products (ManyToManyField): Продукты
        supplier (ForeignKey): Поставщик, связанная модель с другим звеном сети
        debt (Decimal): Задолженность перед поставщиком
        level (int): Уровень звена в иерархии (0: Завод, 1: Розничная сеть, 2: Индивидуальный предприниматель)
        created_at (datetime): Дата и время создания
    Методы:
        get_level(self) -> int:
            Вычисление уровня цепочки. Уровни 0,1,2.
        clean(self) -> None:
            Проверка допустимого уровня звена. Если уровень больше 2 - ValidationError
        save(self, *args, **kwargs) -> None:
            Сохранение уровня и задолженности
    """

    objects: Type[models.Manager]
    LEVEL_CHOICES = [(0, "Завод"), (1, "Розничная сеть"), (2, "Индивидуальный предприниматель")]

    name = models.CharField(max_length=255, verbose_name="Название компании", help_text="Введите название компании")
    contacts = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="networks",
        verbose_name="Контакты",
        help_text="Введите ID звена контактов",
    )
    products = models.ManyToManyField(
        Product, related_name="networks", verbose_name="Продукты", help_text="Введите ID продуктов"
    )
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="networks",
        verbose_name="Поставщик",
        help_text="Введите ID звена поставщика",
    )
    debt = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Задолженность",
        help_text="Введите задолженность перед поставщиком",
    )
    level = models.IntegerField(
        editable=False,
        choices=LEVEL_CHOICES,
        verbose_name="Уровень звена",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")

    def __str__(self) -> str:
        return f"{self.name}"

    def get_level(self) -> int:
        """Вычисление уровня цепочки. Уровни 0,1,2."""
        current = self
        level = 0
        while current.supplier:
            current = current.supplier
            level += 1
            if level >= 3:
                break
        return level

    def clean(self) -> None:
        """Проверка допустимого уровня звена. Если уровень больше 2 - ValidationError"""
        super().clean()
        level = self.get_level()
        max_allowed_level = 2
        if level > max_allowed_level:
            raise ValidationError(
                f"Максимальный допустимый уровень цепочки — {max_allowed_level}. Текущий уровень: {level}."
            )

    def save(self, *args, **kwargs) -> None:
        """Сохранение уровня и задолженности"""
        self.level = self.get_level()
        if self.supplier is None:
            self.debt = 0
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "звено сети"
        verbose_name_plural = "звенья сети"

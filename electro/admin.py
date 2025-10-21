from django.contrib import admin

from .models import Contact, Product


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Класс для работы администратора с контактами
    Атрибуты:
        ordering - сортировка по email
        list_filter - фильтрация: страна, город
        list_display - выводит на экран: email, страна, город
        search_fields - поиск по: email, страна, город
    """

    ordering = ("email",)
    list_filter = ("country", "city",)
    list_display = ("email", "country", "city",)
    search_fields = ("email", "country", "city",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Класс для работы администратора с продуктами
    Атрибуты:
        ordering - сортировка по дате выхода на рынок
        list_display - выводит на экран: название, модель, дата выхода на рынок
        search_fields - поиск по: название, модель
    """

    ordering = ("release_date",)
    list_display = ("name", "model", "release_date",)
    search_fields = ("name", "model",)

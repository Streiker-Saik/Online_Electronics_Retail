from django.contrib import admin

from .models import Contact


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

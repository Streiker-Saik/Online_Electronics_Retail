from typing import Union

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .apps import ElectroConfig
from .models import Contact, Product, Network


app_name = ElectroConfig.name

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


@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    """
    Класс для работы администратора со звеном сети
    Атрибуты:
        ordering - сортировка по дате создания
        list_display - выводит на экран: название, ссылка на поставщика, задолженность, уровень звена, дата создания
        list_filter - фильтрация по: город контакта, уровень звена
        search_fields - поиск по: название,
        actions - clear_debt(очистка задолженности)
    Методы:
        supplier_link(self, obj) -> str:
            Ссылка на Поставщика. При отсутствии поставщика строка 'Нет поставщика'
        clear_debt(self, request, queryset) -> None:
            Очистка задолженности перед поставщиком
    """
    ordering = ("created_at",)
    list_display = ("name", "supplier_link", "debt", "level", "created_at")
    list_filter = ("contacts__city", "level")
    search_fields = ("name",)
    actions = ['clear_debt']

    def supplier_link(self, obj) -> str:
        """Ссылка на Поставщика. При отсутствии поставщика строка 'Нет поставщика'"""
        if obj.supplier:
            url = reverse(f"{app_name}:networks-detail", kwargs={"pk": obj.supplier.id})
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "Нет поставщика"
    supplier_link.short_description = "Поставщик"

    def clear_debt(self, request, queryset) -> None:
        """Очистка задолженности перед поставщиком"""
        queryset.update(debt=0)
    clear_debt.short_description = "Очистить задолженность перед поставщиком"

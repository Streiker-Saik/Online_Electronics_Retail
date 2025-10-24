from decimal import Decimal

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse

from electro.admin import NetworkAdmin
from electro.models import Contact, Network, Product


class NetworkAdminTestCase(TestCase):
    """Представление тестирования в админ панели модель сети"""

    def setUp(self):
        self.contact = Contact.objects.create(
            email="contact1@test.com",
            country="Россия",
            city="Санкт-Петербург",
            street="Невский проспект",
            house_number="20",
        )
        self.product = Product.objects.create(
            name="iPhone 14",
            model="A2649",
            release_date="2022-09-16",
        )
        self.network_zavod = Network.objects.create(
            name="Завод",
            contacts=self.contact,
            supplier=None,
            debt=Decimal("99.99"),
        )
        self.network_retail = Network.objects.create(
            name="Розничная сеть",
            contacts=self.contact,
            supplier=self.network_zavod,
            debt=Decimal("99.99"),
        )
        self.network_zavod.products.add(self.product)
        self.network_retail.products.add(self.product)

        self.admin_instance = NetworkAdmin(Network, None)
        self.factory = RequestFactory()

    def test_supplier_link_with_supplier(self):
        """Тестирование формирования ссылки в поставщике"""
        html = self.admin_instance.supplier_link(self.network_retail)
        url = reverse(f"electro:networks-detail", kwargs={"pk": self.network_zavod.id})
        self.assertIn(f'<a href="{url}">{self.network_zavod.name}</a>', html)
        self.assertEqual(self.admin_instance.supplier_link.short_description, "Поставщик")

    def test_supplier_link_without_supplier(self):
        """Тестирование получения записи когда поставщика нет"""
        html = self.admin_instance.supplier_link(self.network_zavod)
        self.assertIn("Нет поставщика", html)
        self.assertEqual(self.admin_instance.supplier_link.short_description, "Поставщик")

    def test_clear_debt(self):
        """Тестирование проверки очистки задолженности"""
        queryset = Network.objects.filter(
            id__in=[
                self.network_zavod.id,
                self.network_retail.id,
            ]
        )
        self.admin_instance.clear_debt(None, queryset)
        # Обновляем данные БД
        self.network_zavod.refresh_from_db()
        self.network_retail.refresh_from_db()
        self.assertEqual(self.network_zavod.debt, 0)
        self.assertEqual(self.network_retail.debt, 0)

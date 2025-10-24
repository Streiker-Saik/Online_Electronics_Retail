from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from electro.apps import ElectroConfig
from electro.models import Contact, Network, Product

app_name = ElectroConfig.name


class NetworkTestCase(APITestCase):
    """Представление тестирования сети"""

    def setUp(self):
        self.user = User.objects.create(
            username="user",
        )
        self.client.force_authenticate(user=self.user)
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
        self.network_ip = Network.objects.create(
            name="ИП",
            contacts=self.contact,
            supplier=self.network_retail,
            debt=Decimal("123.45"),
        )
        self.network_zavod.products.add(self.product)
        self.network_retail.products.add(self.product)
        self.network_ip.products.add(self.product)

        self.url_list = reverse(f"{app_name}:networks-list")
        self.url_detail = reverse(f"{app_name}:networks-detail", kwargs={"pk": self.network_zavod.id})
        self.url_detail_max_level = reverse(f"{app_name}:networks-detail", kwargs={"pk": self.network_ip.id})

    def test_str_network(self) -> None:
        """Тестирование строкового представления модели сети"""
        network = self.network_zavod
        expected_str = f"{network.name}"
        actual_str = str(Network.objects.get(name=network.name))
        self.assertEqual(expected_str, actual_str)

    def test_networks_list(self) -> None:
        """Тестирование получения списка звеньев сети"""

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        network_zavod = response_data[0]
        self.assertEqual(len(response_data), 3)
        self.assertEqual(network_zavod["id"], self.network_zavod.id)
        self.assertEqual(network_zavod["name"], self.network_zavod.name)
        self.assertEqual(network_zavod["contacts"]["id"], self.contact.id)
        self.assertEqual(network_zavod["contacts"]["email"], self.contact.email)
        self.assertEqual(network_zavod["contacts"]["country"], self.contact.country)
        self.assertEqual(network_zavod["contacts"]["city"], self.contact.city)
        self.assertEqual(network_zavod["contacts"]["street"], self.contact.street)
        self.assertEqual(network_zavod["contacts"]["house_number"], self.contact.house_number)
        self.assertEqual(len(network_zavod["products"]), 1)
        self.assertEqual(network_zavod["products"][0]["id"], self.product.id)
        self.assertEqual(network_zavod["products"][0]["name"], self.product.name)
        self.assertEqual(network_zavod["products"][0]["model"], self.product.model)
        self.assertEqual(network_zavod["products"][0]["release_date"], self.product.release_date)
        self.assertEqual(network_zavod["supplier"], None)
        self.assertEqual(network_zavod["debt"], "0.00")
        self.assertEqual(network_zavod["level"], 0)
        self.assertIn("created_at", network_zavod)

        network_retail = response_data[1]
        self.assertEqual(network_retail["supplier"], self.network_zavod.id)
        self.assertEqual(network_retail["debt"], str(self.network_retail.debt))
        self.assertEqual(network_retail["level"], 1)

    def test_network_create(self) -> None:
        """Тестирование создания звена сети"""
        data = {
            "name": "ИП - тест",
            "contacts": self.contact.id,
            "products": [self.product.id],
            "supplier": self.network_retail.id,
            "debt": "123.45",
        }
        initial_count = Network.objects.count()
        response = self.client.post(self.url_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()
        self.assertEqual(Network.objects.count(), initial_count + 1)
        self.assertIn("id", response_data)
        self.assertIn("created_at", response_data)
        for key in data:
            self.assertEqual(response.json()[key], data[key])

    def test_network_create_error(self) -> None:
        """Тестирование попытки создания звена сети выходящего за допустимый уровень"""
        data = {
            "name": "3 уровень звена",
            "contacts": self.contact.id,
            "products": [self.product.id],
            "supplier": self.network_ip.id,
            "debt": "123.45",
        }
        initial_count = Network.objects.count()

        response = self.client.post(self.url_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertEqual(Network.objects.count(), initial_count)
        self.assertIn("Максимальный допустимый уровень цепочки — 2. Текущий уровень: 3.", response_data)

    def test_get_network(self) -> None:
        """Тестирование получения звена сети по id"""

        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["id"], self.network_zavod.id)
        self.assertEqual(response_data["name"], self.network_zavod.name)
        self.assertEqual(response_data["contacts"], self.contact.id)
        self.assertEqual(response_data["products"], [self.product.id])
        self.assertEqual(response_data["supplier"], None)
        self.assertEqual(response_data["debt"], "0.00")
        self.assertEqual(response_data["level"], 0)
        self.assertIn("created_at", response_data)

    def test_update_network(self) -> None:
        """Тестирование обновления звена сети"""
        data = {
            "name": "Завод ООО",
            "contacts": self.contact.id,
            "products": [self.product.id],
        }
        response = self.client.patch(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["id"], self.network_zavod.id)
        self.assertEqual(response_data["name"], data["name"])
        self.assertEqual(response_data["contacts"], data["contacts"])
        self.assertEqual(response_data["products"], data["products"])
        self.assertEqual(response_data["supplier"], None)
        self.assertEqual(response_data["level"], 0)
        self.assertIn("created_at", response_data)

    def test_partial_update_network(self) -> None:
        """Тестирование частичного обновления звена сети"""
        data = {"name": "Розничная сеть ромашка"}
        response = self.client.patch(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data["id"], self.network_zavod.id)
        self.assertEqual(response_data["name"], data["name"])
        self.assertEqual(response_data["contacts"], self.contact.id)
        self.assertEqual(response_data["products"], [self.product.id])
        self.assertEqual(response_data["supplier"], None)
        self.assertEqual(response_data["level"], 0)
        self.assertIn("created_at", response_data)

    def test_not_update_debt_by_network(self) -> None:
        """Тестирование попытки изменения debt api запросом."""
        original_debt = self.network_zavod.debt

        data = {"debt": "100000.00"}
        response = self.client.patch(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_debt = Network.objects.get(id=self.network_zavod.id).debt
        self.assertEqual(new_debt, original_debt)

    def test_delete_network(self) -> None:
        """Тестирование удаления звена сети"""
        initial_count = Network.objects.count()
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Network.objects.count(), initial_count - 1)

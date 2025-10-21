from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from electro.apps import ElectroConfig
from electro.models import Product


app_name = ElectroConfig.name

class ProductTestCase(APITestCase):
    """Представление тестирования контактов"""

    def setUp(self):
        self.user = User.objects.create(username="user",)
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(
            name="iPhone 14",
            model="A2649",
            release_date="2022-09-16",
        )
        self.url_list = reverse(f"{app_name}:products-list")
        self.url_detail = reverse(f"{app_name}:products-detail", kwargs={"pk": self.product.id})

    def test_str_product(self) -> None:
        """Тестирование строкового представления модели продукта"""
        product = self.product
        expected_str = f"{product.name} ({product.model})"
        actual_str = str(Product.objects.get(name=product.name))
        self.assertEqual(expected_str, actual_str)

    def test_products_list(self) -> None:
        """Тестирование получения списка продуктов"""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            {
                "id": self.product.id,
                "name": self.product.name,
                "model": self.product.model,
                "release_date": self.product.release_date,
            },
            response.json()
        )

    def test_product_create(self) -> None:
        """Тестирование создания контакта"""
        data = {
            "name": "Dell XPS 13",
            "model": "9310",
            "release_date": "2020-11-10",
        }
        initial_count = Product.objects.count()
        response = self.client.post(self.url_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), initial_count + 1)
        self.assertIn("id", response.json())
        for key in data:
            self.assertEqual(response.json()[key], data[key])

    def test_get_product(self) -> None:
        """Тестирование получения продукта по id"""
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.product.id,
                "name": self.product.name,
                "model": self.product.model,
                "release_date": self.product.release_date,
            }
        )

    def test_update_product(self) -> None:
        """Тестирование обновления продукта"""
        data = {
            "name": "iPhone 14 Pro",
            "model": "A26490",
            "release_date": "2022-09-17",
        }
        response = self.client.put(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.product.id,
                "name": data["name"],
                "model": data["model"],
                "release_date": data["release_date"],
            },
        )

    def test_partial_update_product(self) -> None:
        """Тестирование частичного обновления продукта"""
        data = {"name": "iPhone 14 Pro Max"}
        response = self.client.patch(self.url_detail, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.product.id,
                "name": data["name"],
                "model": self.product.model,
                "release_date": self.product.release_date,
            },
        )

    def test_delete_product(self) -> None:
        """Тестирование удаления продукта"""
        initial_count = Product.objects.count()
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), initial_count - 1)


class PermissionsProductTestCase(APITestCase):
    """Представление тестирования продуктов по правам доступа"""

    def setUp(self):
        self.user = User.objects.create(username="user",)
        self.user.is_active = False
        self.user.save()
        self.product = Product.objects.create(
            name="iPhone 14",
            model="A2649",
            release_date="2022-09-16",
        )
        self.url_list = reverse(f"{app_name}:products-list")
        self.url_detail = reverse(f"{app_name}:products-detail", kwargs={"pk": self.product.id})

    def test_not_authenticated(self) -> None:
        """Тестирование доступа не авторизованного пользователя"""
        data = {"test": "test"}

        test_cases = [
            ("get", self.url_list, None),
            ("get", self.url_detail, None),
            ("post", self.url_list, data),
            ("patch", self.url_detail, data),
            ("put", self.url_detail, data),
            ("delete", self.url_detail, None)
        ]
        expected_status = status.HTTP_401_UNAUTHORIZED

        for method, url, data in test_cases:
            with self.subTest(method=method, url=url):
                response = getattr(self.client, method)(url, data=data)
                self.assertEqual(response.status_code, expected_status)

    def test_user_not_action(self) -> None:
        """Тестирование доступа не активного пользователя"""
        self.client.force_authenticate(user=self.user)
        data = {"test": "test"}

        test_cases = [
            ("get", self.url_list, None),
            ("get", self.url_detail, None),
            ("post", self.url_list, data),
            ("patch", self.url_detail, data),
            ("put", self.url_detail, data),
            ("delete", self.url_detail, None)
        ]
        expected_status = status.HTTP_403_FORBIDDEN

        for method, url, data in test_cases:
            with self.subTest(method=method, url=url):
                response = getattr(self.client, method)(url, data=data)
                self.assertEqual(response.status_code, expected_status)

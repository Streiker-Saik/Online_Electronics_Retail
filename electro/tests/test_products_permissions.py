from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from electro.apps import ElectroConfig
from electro.models import Product

app_name = ElectroConfig.name


class PermissionsProductTestCase(APITestCase):
    """Представление тестирования продуктов по правам доступа"""

    def setUp(self):
        self.user = User.objects.create(
            username="user",
        )
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
            ("delete", self.url_detail, None),
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
            ("delete", self.url_detail, None),
        ]
        expected_status = status.HTTP_403_FORBIDDEN

        for method, url, data in test_cases:
            with self.subTest(method=method, url=url):
                response = getattr(self.client, method)(url, data=data)
                self.assertEqual(response.status_code, expected_status)

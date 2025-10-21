from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from electro.models import Contact


class ContactTestCase(APITestCase):
    """Представление тестирования контактов"""

    def setUp(self):
        self.user = User.objects.create(username="user",)
        self.client.force_authenticate(user=self.user)
        self.contact = Contact.objects.create(
            email="contact1@test.com",
            country="Россия",
            city="Санкт-Петербург",
            street="Невский проспект",
            house_number="20"
        )

    def test_str_contacts(self) -> None:
        """Тестирование строкового представления модели"""
        contact = self.contact
        expected_str = f"{contact.email}, {contact.country}, {contact.city}, {contact.street}, {contact.house_number}"
        actual_str = str(Contact.objects.get(email=contact.email))
        self.assertEqual(expected_str, actual_str)

    def test_contacts_list(self) -> None:
        """Тестирование получения списка контактов"""
        response = self.client.get("/contacts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            {
                "id": self.contact.id,
                "email": self.contact.email,
                "country": self.contact.country,
                "city": self.contact.city,
                "street": self.contact.street,
                "house_number": self.contact.house_number,
            }, response.json())

    def test_contact_create(self) -> None:
        """Тестирование создания контакта"""
        data = {
            "email": "contact2@test.com",
            "country": "Россия",
            "city": "Москва",
            "street": "Тверская улица",
            "house_number": "5"
        }
        initial_count = Contact.objects.count()
        response = self.client.post("/contacts/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), initial_count + 1)
        self.assertEqual(
            response.json(),
            {
                "id": initial_count + 1,
                "email": "contact2@test.com",
                "country": "Россия",
                "city": "Москва",
                "street": "Тверская улица",
                "house_number": "5"
            }
        )

    def test_get_contact(self) -> None:
        """Тестирование получения контакта по id"""
        response = self.client.get(f"/contacts/{self.contact.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.contact.id,
                "email": self.contact.email,
                "country": self.contact.country,
                "city": self.contact.city,
                "street": self.contact.street,
                "house_number": self.contact.house_number,
            }
        )

    def test_update_contact(self) -> None:
        """Тестирование обновления контакта"""
        data = {
            "email": "contact1_update@test.com",
            "country": "РФ",
            "city": "Петербург",
            "street": "Невский",
            "house_number": "20а"
        }
        response = self.client.put(f"/contacts/{self.contact.id}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.contact.id,
                "email": data["email"],
                "country": data["country"],
                "city": data["city"],
                "street": data["street"],
                "house_number": data["house_number"],
            },
        )

    def test_partial_update(self) -> None:
        """Тестирование частичного обновления контакта"""
        data = {"house_number": "20а"}
        response = self.client.patch(f"/contacts/{self.contact.id}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.contact.id,
                "email": self.contact.email,
                "country": self.contact.country,
                "city": self.contact.city,
                "street": self.contact.street,
                "house_number": data["house_number"],
            },
        )

    def test_delete_contact(self) -> None:
        """Тестирование удаления контакта"""
        initial_count = Contact.objects.count()
        response = self.client.delete(f"/contacts/{self.contact.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), initial_count - 1)


class PermissionsContactTestCase(APITestCase):
    """Представление тестирования контактов по правам доступа"""

    def setUp(self):
        self.user = User.objects.create(username="user",)
        self.user.is_active = False
        self.user.save()
        self.contact = Contact.objects.create(
            email="contact1@test.com",
            country="Россия",
            city="Санкт-Петербург",
            street="Невский проспект",
            house_number="20"
        )

    def test_not_authenticated(self) -> None:
        """Тестирование доступа не авторизованного пользователя"""
        data = {
            "email": "contact1_update@test.com",
            "country": "РФ",
            "city": "Петербург",
            "street": "Невский",
            "house_number": "20а"
        }

        test_cases = [
            ("get", "/contacts/", None),
            ("get", f"/contacts/{self.contact.id}/", None),
            ("post", "/contacts/", data),
            ("patch", f"/contacts/{self.contact.id}/", data),
            ("put", f"/contacts/{self.contact.id}/", data),
            ("delete", f"/contacts/{self.contact.id}/", None)
        ]
        expected_status = status.HTTP_401_UNAUTHORIZED

        for method, url, data in test_cases:
            with self.subTest(method=method, url=url):
                response = getattr(self.client, method)(url, data=data)
                self.assertEqual(response.status_code, expected_status)

    def test_user_not_action(self) -> None:
        """Тестирование доступа не активного пользователя"""
        self.client.force_authenticate(user=self.user)
        data = {
            "email": "contact1_update@test.com",
            "country": "РФ",
            "city": "Петербург",
            "street": "Невский",
            "house_number": "20а"
        }

        test_cases = [
            ("get", "/contacts/", None),
            ("get", f"/contacts/{self.contact.id}/", None),
            ("post", "/contacts/", data),
            ("patch", f"/contacts/{self.contact.id}/", data),
            ("put", f"/contacts/{self.contact.id}/", data),
            ("delete", f"/contacts/{self.contact.id}/", None)
        ]
        expected_status = status.HTTP_403_FORBIDDEN

        for method, url, data in test_cases:
            with self.subTest(method=method, url=url):
                response = getattr(self.client, method)(url, data=data)
                self.assertEqual(response.status_code, expected_status)

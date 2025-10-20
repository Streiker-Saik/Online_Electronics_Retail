from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    """
    Команда для создания суперпользователя по ключам username, password.
    Если не указано, то: username='admin', password='admin'.
    Методы:
        add_arguments(self, parser):
            Добавляет аргументы команды: username, password.
        handle(self, *args, **options) -> None:
            Обрабатывает команду для создания суперпользователя.
    """

    help = "Создание суперпользователя с username, password."

    def add_arguments(self, parser):
        """Добавляет аргументы команды: username, password."""
        parser.add_argument("--username", type=str, default="admin", help="Логин для входа суперпользователя")
        parser.add_argument("--password", type=str, default="admin", help="Пароль для входя суперпользователя")

    def handle(self, *args, **options) -> None:
        """Обрабатывает команду для создания суперпользователя."""
        username = options["username"]
        password = options["password"]
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR("Суперпользователь с данным логином уже существует."))
        else:
            User.objects.create_superuser(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(f"Суперпользователь {username} создан успешно!"))

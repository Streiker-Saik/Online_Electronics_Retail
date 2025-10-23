from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from electro.models import Contact, Network, Product
from electro.permissions import IsActiveUser
from electro.serializaters import (ContactSerializer, NetworkListSerializer, NetworkSerializer,
                                   NetworkUpdateSerializer, ProductSerializer)


class ContactViewSet(ModelViewSet):
    """
    Представление набора действий для модели Contact.
    Позволяет выполнять операции с контактами:
        отображение списка, создание, отображение, полное обновление, частичное обновление, удаление.
    """

    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    permission_classes = [IsAuthenticated, IsActiveUser]

    @swagger_auto_schema(operation_description="Представление для получения списка всех контактов.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для получения контакта.")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для создания нового контакта")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для полного обновления контакта по идентификатору")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для частичного обновления контакта по идентификатору")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для удаления контакта.")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ProductViewSet(ModelViewSet):
    """
    Представление набора действий для модели Product.
    Позволяет выполнять операции с контактами:
        отображение списка, создание, отображение, полное обновление, частичное обновление, удаление.
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsActiveUser]

    @swagger_auto_schema(operation_description="Представление для получения списка всех продуктов.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для получения продукта.")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для создания нового продукта")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для полного обновления продукта по идентификатору")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для частичного обновления продукта по идентификатору")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для удаления продукта.")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class NetworkViewSet(ModelViewSet):
    """
    Представление набора действий для модели Network.
    Фильтрация по стране.
    Позволяет выполнять операции с контактами:
        отображение списка, создание, отображение, полное обновление, частичное обновление, удаление.
    Методы:
        get_serializer_class(self):
            Получение сериализатора:
                "list" - получение полного сериализатора с продуктами и контактами
                "update", "partial_update" - закрыт доступ к полю задолженности
                другие - получения сериализатора со всеми полями

    """

    queryset = Network.objects.all()
    permission_classes = [IsAuthenticated, IsActiveUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["contacts__country"]

    def get_serializer_class(self):
        """
        Получение сериализатора:
            "list" - получение полного сериализатора с продуктами и контактами
            "update", "partial_update" - закрыт доступ к полю задолженности
            другие - получения сериализатора со всеми полями
        """
        if self.action in ("list",):
            return NetworkListSerializer
        elif self.action in ("update", "partial_update"):
            return NetworkUpdateSerializer
        return NetworkSerializer

    @swagger_auto_schema(operation_description="Представление для получения списка всех звеньев цепи.")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для получения звена цепи.")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для создания нового звена цепи")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для полного обновления звена цепи по идентификатору")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для частичного обновления звена цепи по идентификатору")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Представление для удаления звена цепи.")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

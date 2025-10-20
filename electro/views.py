from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from electro.models import Contact
from electro.permissions import IsActiveUser
from electro.serializaters import ContactSerializer


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

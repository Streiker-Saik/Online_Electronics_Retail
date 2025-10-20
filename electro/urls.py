from django.urls import path
from rest_framework.routers import DefaultRouter

from electro.apps import ElectroConfig
from electro.views import ContactViewSet

app_name = ElectroConfig.name

router = DefaultRouter()
router.register(r"contact", ContactViewSet, basename="contact")

urlpatterns = []

urlpatterns += router.urls

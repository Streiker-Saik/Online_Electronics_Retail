from django.urls import path, include
from rest_framework.routers import DefaultRouter

from electro.apps import ElectroConfig
from electro.views import ContactViewSet

app_name = ElectroConfig.name

router = DefaultRouter()
router.register(r"contacts", ContactViewSet, basename="contacts")

urlpatterns = [path("api/v1.0/", include(router.urls))]

# urlpatterns += router.urls

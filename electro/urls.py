from django.urls import path, include
from rest_framework.routers import DefaultRouter

from electro.apps import ElectroConfig
from electro.views import ContactViewSet, ProductViewSet, NetworkViewSet

app_name = ElectroConfig.name

router = DefaultRouter()
router.register(r"contacts", ContactViewSet, basename="contacts")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"networks", NetworkViewSet, basename="networks")

urlpatterns = [path("api/v1.0/", include(router.urls))]

# urlpatterns += router.urls

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet, CategoryViewSet


router = DefaultRouter()  # ----> Api Root a error day na...link day...
router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)


urlpatterns = [
    path("", include(router.urls)),
    # --> Aro path add kora jabe....
]

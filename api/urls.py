from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from product.views import ProductViewSet, CategoryViewSet, ReviewViewSet


router = routers.DefaultRouter()  # ----> Api Root a error day na...link day...
router.register("products", ProductViewSet, basename="products")
router.register("categories", CategoryViewSet)

product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", ReviewViewSet, basename="product-review")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from product.views import ProductViewSet, CategoryViewSet, ReviewViewSet
from order.views import CartViewSet, CartItemViewSet, OrderViewSet


router = routers.DefaultRouter()  # ----> Api Root a error day na...link day...
router.register("products", ProductViewSet, basename="products")
router.register("categories", CategoryViewSet)
router.register("carts", CartViewSet, basename="carts")
router.register("orders", OrderViewSet, basename="orders")

product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", ReviewViewSet, basename="product-review")

cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", CartItemViewSet, basename="cart-item")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_router.urls)),
    path("", include(cart_router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]

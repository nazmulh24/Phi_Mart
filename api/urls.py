from django.urls import path, include


urlpatterns = [
    path("products/", include("product.urls_product")),
    path("categories/", include("product.urls_category")),
]

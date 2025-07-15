from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from product.views import ProductViewSet, CategoryViewSet

# router = SimpleRouter()
router = DefaultRouter()  # ----> Api Root a error day na...link day...
router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)

# urlpatterns = router.urls  #----> Eivabe na likhe nicer moto lekha jay...

urlpatterns = [
    path("", include(router.urls)),
    # --> Aro path add kora jabe....
]

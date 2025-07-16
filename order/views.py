from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)

from order.models import Cart
from order.serializers import CartSerializer


# ---> ModelViewSet use kori nai---> couse-- amra ListModelMixin use korte cai na...
class CartViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

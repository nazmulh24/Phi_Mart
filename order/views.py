from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated

from order.models import Cart, CartItem, Order, OrderItem
from order.serializers import (
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    OrderSerializer,
)


# ---> ModelViewSet use kori nai---> couse-- amra ListModelMixin use korte cai na...
class CartViewSet(
    CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):
    # queryset = Cart.objects.all()
    def get_queryset(self):
        return Cart.objects.prefetch_related("items__product").filter(
            user=self.request.user
        )

    serializer_class = CartSerializer

    permission_classes = [IsAuthenticated]


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        queryset = CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])
        return queryset

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer


class OrderViewSet(ModelViewSet):
    # queryset = Order.objects.all()
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related("items__product").all()
        return Order.objects.prefetch_related("items__product").filter(
            user=self.request.user
        )

    serializer_class = OrderSerializer

    permission_classes = [IsAuthenticated]

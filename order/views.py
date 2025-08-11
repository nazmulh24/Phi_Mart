from django.http import HttpResponseRedirect
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from order.services import OrderService
from order.models import Cart, CartItem, Order, OrderItem
from order.serializers import (
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    OrderSerializer,
    OrderCreateSerializer,
    UpdateOrderSerializer,
)
from order import serializers as orderSz
from django.conf import settings as main_settings

from sslcommerz_lib import SSLCOMMERZ


# ---> ModelViewSet use kori nai---> couse-- amra ListModelMixin use korte cai na...
class CartViewSet(
    CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):
    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related("items__product").filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    serializer_class = CartSerializer

    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        existing_cart = Cart.objects.filter(user=request.user).first()
        if existing_cart:
            serializer = self.get_serializer(existing_cart)
            return Response(serializer.data, status=200)
        return super().create(request, *args, **kwargs)


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        queryset = CartItem.objects.select_related("product").filter(
            cart_id=self.kwargs.get("cart_pk")
        )
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, "swagger_fake_view", False):
            return context
        return {"cart_id": self.kwargs["cart_pk"]}

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer


class OrderViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete", "patch", "head", "options"]

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order, user=request.user)
        return Response({"status": "Order canceled"})

    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = orderSz.UpdateOrderSerializer(
            order, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": f"Order status updated to {request.data['status']}"})

    def get_permissions(self):
        if self.action in ["update_status", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Order.objects.none()
        if self.request.user.is_staff:
            return Order.objects.prefetch_related("items__product").all()
        return Order.objects.prefetch_related("items__product").filter(
            user=self.request.user
        )

    def get_serializer_class(self):
        if self.action == "cancel":
            return orderSz.EmptySerializer
        if self.action == "create":
            return OrderCreateSerializer
        elif self.action == "update_status":
            return UpdateOrderSerializer
        return OrderSerializer

    def get_serializer_context(self):
        if getattr(self, "swagger_fake_view", False):
            return super().get_serializer_context()
        return {"user_id": self.request.user.id, "user": self.request.user}


@api_view(["POST"])
def initiate_payment(request):
    user = request.user
    amount = request.data.get("amount")
    order_id = request.data.get("orderId")
    number_of_items = request.data.get("numItems", 1)

    settings = {
        "store_id": "nazmu689918a6d45d1",
        "store_pass": "nazmu689918a6d45d1@ssl",
        "issandbox": True,
    }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body["total_amount"] = amount
    post_body["currency"] = "BDT"
    post_body["tran_id"] = f"txn_{order_id}"
    post_body["success_url"] = f"{main_settings.BACKEND_URL}/api/v1/payment/success/"
    post_body["fail_url"] = f"{main_settings.BACKEND_URL}/api/v1/payment/fail/"
    post_body["cancel_url"] = f"{main_settings.BACKEND_URL}/api/v1/payment/cancel/"
    post_body["emi_option"] = 0
    post_body["cus_name"] = f"{user.first_name} {user.last_name}"
    post_body["cus_email"] = user.email
    post_body["cus_phone"] = user.phone_number or "N/A"
    post_body["cus_add1"] = user.address or "N/A"
    post_body["cus_city"] = "Dhaka"
    post_body["cus_country"] = "Bangladesh"
    post_body["shipping_method"] = "No"
    post_body["multi_card_name"] = ""
    post_body["num_of_item"] = number_of_items
    post_body["product_name"] = "E-commerce Product"
    post_body["product_category"] = "General"
    post_body["product_profile"] = "general"

    response = sslcz.createSession(post_body)  # API response
    print(response)

    if response.get("status") == "SUCCESS":
        return Response({"payment_url": response["GatewayPageURL"]}, status=200)
    return Response({"error": "Payment initiation failed"}, status=400)


@api_view(["POST"])
def payment_success(request):
    print("Inside success")
    order_id = request.data.get("tran_id").split("_")[1]
    order = Order.objects.get(id=order_id)
    order.status = "Ready To Ship"
    order.save()
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/orders/")


@api_view(["POST"])
def payment_cancel(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/orders/")


@api_view(["POST"])
def payment_fail(request):
    print("Inside fail")
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/orders/")

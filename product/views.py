from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from api.permissions import IsAdminOrReadOnly

from product.permissions import IsReviewAuthorOrReadonly
from product.paginations import DefaultPagination
from product.filters import ProductFilter
from product.models import Product, ProductImage, Category, Review
from product.serializers import (
    ProductSerializer,
    ProductImageSerializer,
    CategorySerializer,
    ReviewSerializer,
)
from django.db.models import Count

from drf_yasg.utils import swagger_auto_schema


class ProductViewSet(ModelViewSet):
    """
    API endpoint for managing products in the e-commerce store
     - Allows authenticated admin to create, update, and delete products
     - Allows users to browse and filter product
     - Support searching by name, description, and category
     - Support ordering by price and updated_at
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]  # --> Ok for Normal Use..

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at", "updated_at"]

    @swagger_auto_schema(operation_summary="Retrive a list of products")
    def list(self, request, *args, **kwargs):
        """Retrive all the products"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a product by admin",
        operation_description="This allow an admin to create a product",
        request_body=ProductSerializer,
        responses={201: ProductSerializer, 400: "Bad Request"},
    )
    def create(self, request, *args, **kwargs):
        """Only authenticated admin can create product"""
        return super().create(request, *args, **kwargs)


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get("product_pk"))

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs.get("product_pk"))


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count("products")).all()
    serializer_class = CategorySerializer

    permission_classes = [IsAdminOrReadOnly]


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadonly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def perform_update(self, serializer): # -----> 3rd way..
    #     serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get("product_pk"))

    def get_serializer_context(self):
        return {"product_id": self.kwargs.get("product_pk")}

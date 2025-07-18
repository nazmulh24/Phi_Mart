from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from api.permissions import IsAdminOrReadOnly

from product.paginations import DefaultPagination
from product.filters import ProductFilter
from product.models import Product, Category, Review
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from django.db.models import Count


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    pagination_class = DefaultPagination
    # permission_classes = [IsAdminUser]
    permission_classes = [IsAdminOrReadOnly]

    # def get_permissions(self):
    #     if self.request.method in ["GET", "HEAD", "OPTIONS"]:
    #         return [AllowAny()]
    #     return [IsAdminUser()]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at", "updated_at"]

    # ---> Custom filter for delete an item...|--> delete not allow when--> product>10
    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock > 10:
            return Response(
                {"message": "Product with stock more than 10 could't be delete !"}
            )
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count("products")).all()
    serializer_class = CategorySerializer

    permission_classes = [IsAdminOrReadOnly]


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.filter(product_id=self.kwargs["product_pk"])
        return queryset

    # __In-Below__|----> Automatic id ta get korlam (oi product tar)...
    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}

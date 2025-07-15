from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Category
from product.serializers import ProductSerializer, CategorySerializer
from django.db.models import Count


@api_view(["GET", "POST"])
def view_products(request):
    if request.method == "GET":
        products = Product.objects.select_related("category").all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ProductSerializer(data=request.data)  # --> Deserializer

        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view()
def view_specific_products(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def view_categories(request):
    if request.method == "GET":
        categories = Category.objects.annotate(product_count=Count("products")).all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = CategorySerializer(data=request.data)  # --> Deserializer

        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view()
def view_specific_categories(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)

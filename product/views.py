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


@api_view(["GET", "PUT", "DELETE"])
def view_specific_products(request, id):
    if request.method == "GET":
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    if request.method == "PUT":
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "DELETE":
        product = get_object_or_404(Product, pk=id)
        copy_product = product
        product.delete()
        serializer = ProductSerializer(copy_product)  # --> Product Details dekhar jonno
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


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

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from product.models import Product, Category
from product.serializers import ProductSerializer, CategorySerializer
from django.db.models import Count


# @api_view(["GET", "POST"])
# def view_products(request):
#     if request.method == "GET":
#         products = Product.objects.select_related("category").all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)

#     if request.method == "POST":
#         serializer = ProductSerializer(data=request.data)  # --> Deserializer

#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


class ViewProducts(APIView):
    def get(self, request):
        products = Product.objects.select_related("category").all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)  # --> Deserializer
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["GET", "PUT", "DELETE"])
# def view_specific_product(request, id):
#     product = get_object_or_404(Product, pk=id)

#     if request.method == "GET":
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)

#     if request.method == "PUT":
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     if request.method == "DELETE":
#         copy_product = product
#         product.delete()
#         serializer = ProductSerializer(copy_product)  # --> Product Details dekhar jonno
#         return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class ViewSpecificProduct(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        copy_product = product
        product.delete()
        serializer = ProductSerializer(copy_product)  # --> Product Details dekhar jonno
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


# @api_view(["GET", "POST"])
# def view_categories(request):
#     if request.method == "GET":
#         categories = Category.objects.annotate(product_count=Count("products")).all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)

#     if request.method == "POST":
#         serializer = CategorySerializer(data=request.data)  # --> Deserializer

#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


class ViewCategory(APIView):
    def get(self, request):
        categories = Category.objects.annotate(product_count=Count("products")).all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)  # --> Deserializer
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["GET", "PUT", "DELETE"])
# def view_specific_category(request, pk):
#     category = get_object_or_404(
#         Category.objects.annotate(product_count=Count("products")), pk=pk
#     )

#     if request.method == "GET":
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)

#     if request.method == "PUT":
#         serializer = CategorySerializer(category, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     if request.method == "DELETE":
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class ViewSpecificCategory(APIView):
    # ---> Defining same data using method...
    def get_category(self, pk):
        return get_object_or_404(
            Category.objects.annotate(product_count=Count("products")), pk=pk
        )

    def get(self, request, pk):
        category = self.get_category(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_category(pk)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        category = self.get_category(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

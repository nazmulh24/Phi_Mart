from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Category
#


@api_view()
def view_specific_products(request, id):
    # try:
    #     product = Product.objects.get(pk=id)
    #     product_dict = {
    #         'id' : product.id,
    #         'name' : product.name,
    #         'price': product.price,
    #     }
    #     return Response(product_dict)
    # except Product.DoesNotExist:
    #     return Response({"message" : "Product does not exist..."}, status=status.HTTP_404_NOT_FOUND)
    
    """
    ------> get_object_or_404 use korle... try-except use kora lagbe na...
    """
    product = get_object_or_404(Product, pk=id)
    product_dict = {
        'id' : product.id,
        'name' : product.name,
        'price': product.price,
    }
    return Response(product_dict)



@api_view()
def view_categories(request):
    return Response({"message" : "Category"})

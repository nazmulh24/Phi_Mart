from rest_framework.decorators import api_view
from rest_framework.response import Response
#


@api_view()
def view_products(request):
    return Response({"message" : "Product"})

@api_view()
def view_categories(request):
    return Response({"message" : "Category"})

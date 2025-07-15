from rest_framework import serializers
from decimal import Decimal
from product.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "product_count"]

    product_count = serializers.IntegerField()  # --> views.view_categories(annotate())


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "category",
            "price_with_tax",
        ]

    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    # category = serializers.HyperlinkedRelatedField(
    #     queryset=Category.objects.all(), view_name="specific-category"
    # )
    # category = CategorySerializer()

    def calculate_tax(self, product):
        return round(product.price * Decimal(1.10), 2)

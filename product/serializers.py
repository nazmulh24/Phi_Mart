from rest_framework import serializers
from decimal import Decimal
from product.models import Product, ProductImage, Category, Review

from django.contrib.auth import get_user_model


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "product_count"]

    product_count = serializers.IntegerField(
        read_only=True
    )  # --> views.view_categories(annotate()) theke asse.....


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

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError("Price could't be negative !")
        return price


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image"]


class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name="full_name")

    class Meta:
        model = get_user_model()
        fields = ["id", "name"]

    def full_name(self, obj):
        return obj.get_full_name()


class ReviewSerializer(serializers.ModelSerializer):
    # user = SimpleUserSerializer() #--> 1st way..
    user = serializers.SerializerMethodField(method_name="get_user")  # --> 2nd way..

    class Meta:
        model = Review
        fields = ["id", "user", "rating", "product", "comment"]
        read_only_fields = ["user", "product"]

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data

    def create(self, validated_data):
        product_id = self.context["product_id"]
        review = Review.objects.create(product_id=product_id, **validated_data)
        return review

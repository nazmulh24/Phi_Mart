from rest_framework import serializers
from decimal import Decimal


"""
Key reasons to use serializers :

  Data Conversion --> They transform Django models or Python objects into JSON for APIs, and vice versa.
  Validation --> They validate incoming data before saving it to the database, ensuring data integrity.
  Custom Representation --> You can control exactly how your data is exposed via the API (e.g., renaming fields, adding computed fields).
  Security --> By specifying which fields are exposed, you prevent leaking sensitive data.
"""


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, source="price")

    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    
    def calculate_tax(self, product):
        return round(product.price * Decimal(1.10), 2)
    

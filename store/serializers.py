from rest_framework import serializers
from decimal import Decimal
from .models import *

class Product_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'price_with_tax']

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product):
        return product.price * Decimal(1.1)
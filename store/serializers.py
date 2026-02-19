from rest_framework import serializers
from decimal import Decimal
from .models import *

# Collection Serializer
class Collection_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
    
    products_count = serializers.SerializerMethodField(method_name='count_products')
    
    def count_products(self, collection):
        return collection.product_set.count()

# Product Serializer
class Product_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'inventory', 'collection', 'price_with_tax']

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product):
        return product.price * Decimal(1.1)
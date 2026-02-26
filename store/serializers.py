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
        fields = ['id', 'title', 'description', 'price', 'price_with_tax', 'inventory', 'collection']

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product):
        return product.price * Decimal(1.1)
    
class SimpleProduct_serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price']
    
# Review Serializer
class Review_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'comment', 'rating', 'created_at', 'product', 'customer']

# Cart and CartItem Serializers
class CartItem_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    product = SimpleProduct_serializer()
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')

    def calculate_total_price(self, cart_item):
        return cart_item.product.price * cart_item.quantity

class AddCartItem_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']
    
    product_id = serializers.IntegerField()
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, product_id=product_id, quantity=quantity)

        return self.instance

class UpdateCartItem_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class Cart_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'cartitem_set', 'total_price']
    
    id = serializers.UUIDField(read_only=True)
    cartitem_set = CartItem_Serializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')

    def calculate_total_price(self, cart):
        return sum([item.product.price * item.quantity for item in cart.cartitem_set.all()])

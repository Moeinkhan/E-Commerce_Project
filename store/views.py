from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveDestroyAPIView
from rest_framework import status
from .models import *
from .serializers import *
from .filters import ProductFilter

# Collection Endpoints
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = Collection_Serializer

class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = Collection_Serializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.product_set.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response()


# Product Endpoints
class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = Product_Serializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'last_update']

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = Product_Serializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitem_set.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response()
    
# Review Endpoints
class ReviewList(ListCreateAPIView):
    serializer_class = Review_Serializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

class ReviewDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = Review_Serializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    
# Cart Endpoints
class CartList(CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = Cart_Serializer

class CartDetail(RetrieveDestroyAPIView):
    queryset = Cart.objects.prefetch_related('cartitem_set__product').all()
    serializer_class = Cart_Serializer

class CartItemList(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItem_Serializer
        return CartItem_Serializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
    
class CartItemDetail(RetrieveUpdateDestroyAPIView):
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateCartItem_Serializer
        return CartItem_Serializer
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
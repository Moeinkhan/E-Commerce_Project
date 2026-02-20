from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from .models import *
from .serializers import *

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

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = Product_Serializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitem_set.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response()
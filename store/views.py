from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from .serializers import *

# Collection Endpoints
class CollectionList(APIView):
    def get(self, request):
        queryset = Collection.objects.all()
        serializer = Collection_Serializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = Collection_Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CollectionDetail(APIView):
    def get(self, request, id):
        collection = get_object_or_404(Collection, pk=id)
        serializer = Collection_Serializer(collection)
        return Response(serializer.data)
    
    def put(self, request, id):
        collection = get_object_or_404(Collection, pk=id)
        serializer = Collection_Serializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        collection = get_object_or_404(Collection, pk=id)
        if collection.product_set.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response()


# Product Endpoints
class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.all()
        serializer = Product_Serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = Product_Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = Product_Serializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = Product_Serializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem_set.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response()
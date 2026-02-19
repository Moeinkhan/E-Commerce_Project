from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import Product_Serializer

@api_view()
def product_list(request):
    queryset = Product.objects.all()
    serializer = Product_Serializer(queryset, many=True)
    return Response(serializer.data)

@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = Product_Serializer(product)
    return Response(serializer.data)
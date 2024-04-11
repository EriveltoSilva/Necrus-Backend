from django.shortcuts import render
from rest_framework import viewsets
from apps.ecommerce.models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """ Enviando todos os productos """
    queryset = Product.objects.filter(is_published=True)
    serializer_class = ProductSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    """ Enviando todas as categorias de Produtos """
    queryset = ProductCategory.objects.filter(is_published=True)
    serializer_class = ProductCategorySerializer

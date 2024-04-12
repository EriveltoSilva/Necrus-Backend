from django.shortcuts import render
from rest_framework import viewsets, generics
from apps.ecommerce.models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCategorySerializer, ProductsByCategorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication

class ProductViewSet(viewsets.ModelViewSet):
    """ Enviando todos os productos """
    queryset = Product.objects.filter(is_published=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]

class ProductCategoryViewSet(viewsets.ModelViewSet):
    """ Enviando todas as categorias de Produtos """
    queryset = ProductCategory.objects.filter(is_published=True)
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]

class ProductsByCategoryList(generics.ListAPIView):
    """ Lista de Produtos Pela Categoria """
    def get_queryset(self):
        queryset = Product.objects.filter(categories__id=self.kwargs['pk'])
        return queryset
    
    serializer_class = ProductsByCategorySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
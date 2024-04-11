from rest_framework import serializers
from apps.ecommerce.models import Product, ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = [
            'id', 'title', 'slug',
            'description', 'image', 'created_at',]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug',
            'description', 'image', 'price',
            'old_price', 'in_stock', 'created_at',]


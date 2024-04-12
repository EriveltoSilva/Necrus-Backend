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
            'description','categories', 'image', 'price',
            'old_price', 'in_stock', 'created_at',]


class ProductsByCategorySerializer(serializers.ModelSerializer):
    # categories = serializers.ReadOnlyField(source='category.title')
    class Meta:
        model= Product
        fields = [
            'id', 'title', 'slug',
            'description', 'image', 'categories','price',
            'old_price', 'in_stock', 'created_at',]
        
        # 8b8f5cb3-89ce-447b-bad4-c6f00daffbf8
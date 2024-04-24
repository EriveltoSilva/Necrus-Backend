from rest_framework import serializers

from .models import Category, Product, Gallery, Specification, Size, Color
from .models import Cart, CartOrder, CartOrderItem, ProductFaq, Review, Wishlist, Notification, Coupon

from apps.vendor.serializers import VendorSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

                            

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
    
    def __init__(self, *args, **kwargs) -> None:
            super(CartSerializer, self).__init__(*args, **kwargs)
            request = self.context.get("request")
            if request and request.method == 'POST':
                self.Meta.depth = 0
            else:
                self.Meta.depth = 3


class CartOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartOrder
        fields = '__all__'
    
    def __init__(self, *args, **kwargs) -> None:
            super(CartOrderSerializer, self).__init__(*args, **kwargs)
            request = self.context.get("request")
            if request and request.method == 'POST':
                self.Meta.depth = 0
            else:
                self.Meta.depth = 3

class CartOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartOrderItem
        fields = '__all__'
    
    def __init__(self, *args, **kwargs) -> None:
            super(CartOrderItemSerializer, self).__init__(*args, **kwargs)
            request = self.context.get("request")
            if request and request.method == 'POST':
                self.Meta.depth = 0
            else:
                self.Meta.depth = 3


class ProductFaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFaq
        fields = '__all__'
    
    def __init__(self, *args, **kwargs) -> None:
            super(ProductFaqSerializer, self).__init__(*args, **kwargs)
            request = self.context.get("request")
            if request and request.method == 'POST':
                self.Meta.depth = 0
            else:
                self.Meta.depth = 3

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
    
    def __init__(self, *args, **kwargs) -> None:
            super(ReviewSerializer, self).__init__(*args, **kwargs)
            request = self.context.get("request")
            if request and request.method == 'POST':
                self.Meta.depth = 0
            else:
                self.Meta.depth = 3


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'
    
    def __init__(self, *args, **kwargs) -> None:
            super(WishlistSerializer, self).__init__(*args, **kwargs)
            request = self.context.get("request")
            if request and request.method == 'POST':
                self.Meta.depth = 0
            else:
                self.Meta.depth = 3

                
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
    
    def __init__(self, *args, **kwargs) -> None:
            super(NotificationSerializer, self).__init__(*args, **kwargs)
            request = self.context.get("request")
            if request and request.method == 'POST':
                self.Meta.depth = 0
            else:
                self.Meta.depth = 3


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
    
    def __init__(self, *args, **kwargs) -> None:
            super(CouponSerializer, self).__init__(*args, **kwargs)
            request = self.context.get("request")
            if request and request.method == 'POST':
                self.Meta.depth = 0
            else:
                self.Meta.depth = 3


class ProductSerializer(serializers.ModelSerializer):
    gallery = GallerySerializer(many=True, read_only=True)
    color = ColorSerializer(many=True, read_only=True)
    specification = SpecificationSerializer(many=True, read_only=True)
    size = SizeSerializer(many=True, read_only=True)
    review = ReviewSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    vendor = VendorSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'image','description',
            'price', 'old_price',
            'shipping_amount', 'stock_quantity', 'is_active',
            'in_stock', 'status', 'featured', 'views', 
            'rating', 'product_rating', 'rating_count',
            'category','vendor', 'gallery', 'color', 'specification',
            'size', 'created_at', 'review',
            ]

        def __init__(self, *args, **kwargs) -> None:
            super(ProductSerializer, self).__init__(*args, **kwargs)
            request = self.context.get("request")
            if request and request.method == 'POST':
                self.Meta.depth = 0
            else:
                self.Meta.depth = 3
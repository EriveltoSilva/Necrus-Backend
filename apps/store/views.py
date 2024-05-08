from django.shortcuts import render

from apps.userauths.models import User

from .models import Product, Category, Cart, CartOrder, CartOrderItem, Tax
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartOrderSerializer, CartOrderItemSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from decimal import Decimal

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        slug = self.kwargs['slug']
        return Product.objects.get(slug=slug)

class CartAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        payload = request.data
        product_id = payload['product_id']
        quantity = payload['quantity']
        price = payload['price']
        country = payload['country'].upper()
        color = payload['color']
        size = payload['size']
        cart_id = payload['cart_id']
        user_id = payload['user_id']
        shipping_amount = payload['shipping_amount']
        
        product = Product.objects.get(id=product_id)
        user = None if user_id == "undefined" else User.objects.get(id=user_id)

        tax = Tax.objects.filter(country__icontains=country).first()
        tax_rate = (tax.rate / 100) if tax else 0

        cart = Cart.objects.filter(cart_id=cart_id, product=product).first()
        if not cart:
            cart = Cart()
        
        cart.product = product
        cart.user = user
        cart.quantity = int(quantity)
        cart.price = price
        cart.sub_total = Decimal(price) * int(quantity)
        cart.shipping_amount =Decimal(shipping_amount) * int(quantity)
        cart.tax_fee = int(quantity) * Decimal(tax_rate)
        cart.color = color
        cart.size = size
        cart.country = country.upper()
        cart.cart_id = cart_id

        service_fee_percentage = 10 / 100
        cart.service_fee = Decimal(service_fee_percentage) * cart.sub_total
        cart.total = cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee
        cart.save()
        return Response({"status":"success", "message": "Cart updated success"}, status=status.HTTP_200_OK)
        # return super().create(request, *args, **kwargs)

# class CartOrderAPIView(generics.ListAPIView):
#     queryset = CartOrder.objects.all()
#     serializer_class = CartOrderSerializer
#     permission_classes = [AllowAny]

# class CartOrderItemAPIView(generics.ListAPIView):
#     queryset = CartOrderItem.objects.all()
#     serializer_class = CartOrderItemSerializer
#     permission_classes = [AllowAny]
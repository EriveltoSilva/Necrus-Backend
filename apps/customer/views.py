import math
import random
from . import utils
from decimal import Decimal
from django.db.models import Q
from django.conf import settings
from apps.userauths.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.store.serializers import CouponSerializer, NotificationSerializer, ReviewSerializer
from apps.store.models import Product, Category, Cart, CartOrder, CartOrderItem, Tax, Coupon, Notification, Review, Wishlist
from apps.store.serializers import ProductSerializer, CategorySerializer, CartSerializer, CartOrderSerializer, CartOrderItemSerializer


class OrdersAPIView(generics.ListAPIView):
    serializer_class = CartOrderSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        orders = CartOrder.objects.filter(buyer=user, payment_status='paid')
        return orders

class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CartOrderSerializer
    permission_classes = (AllowAny,)

    def get_object(self, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        order_oid = self.kwargs.get('order_oid')
        user = User.objects.get(id=user_id)
        order = CartOrder.objects.get(buyer=user, oid=order_oid, payment_status='paid')
        return order
    
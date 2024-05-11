from decimal import Decimal

from apps.userauths.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Product, Category, Cart, CartOrder, CartOrderItem, Tax, Coupon
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartOrderSerializer, CartOrderItemSerializer
from .serializers import CouponSerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_object(self):
        slug = self.kwargs['slug']
        return Category.objects.get(slug=slug)

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
        
        product = Product.objects.filter(id=product_id).first()
        user = None if user_id == "undefined" else User.objects.get(id=user_id)
        print(f"{user}".rjust(100))
        
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
        cart.shipping_amount = Decimal(shipping_amount) * int(quantity)
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

class CartListAPIView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    queryset = Cart.objects.all()

    def get_queryset(self, *args, **kwargs):
        cart_id = self.kwargs.get('cart_id')
        user_id = self.kwargs.get('user_id')

        if user_id is not None:
            user = User.objects.get(id=user_id)
            queryset = Cart.objects.filter(user=user, cart_id=cart_id)
        else:
            queryset = Cart.objects.filter(cart_id=cart_id)
        return queryset
    
class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    lookup_field = "cart_id"

    def get_queryset(self,*args,**kwargs):
        cart_id = self.kwargs.get('cart_id')
        user_id = self.kwargs.get('user_id')

        if user_id is not None:
            user = User.objects.get(id=user_id)
            queryset = Cart.objects.filter(user=user, cart_id=cart_id)
        else:
            queryset = Cart.objects.filter(cart_id=cart_id)
        return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset(*args, **kwargs)

        total_shipping_amount = 0.0
        total_tax_fee = 0.0
        total_service_fee = 0.0
        total_sub_total = 0.0
        total_total = 0.0

        for cart_item in queryset:
            total_shipping_amount += float(cart_item.shipping_amount)
            total_tax_fee += float(cart_item.tax_fee)
            total_service_fee += float(cart_item.service_fee)
            total_sub_total += float(cart_item.sub_total)
            total_total += round(float(cart_item.total), 2)

        data = {
            'shipping_amount': round(total_shipping_amount, 2),
            'tax_fee': total_tax_fee,
            'service_fee': total_service_fee,
            'sub_total': total_sub_total,
            'total': total_total,
        }

        return Response(data, status.HTTP_200_OK)

class CartItemDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    lookup_field = 'cart_id'

    def get_object(self):
        cart_id = self.kwargs.get('cart_id')
        user_id = self.kwargs.get('user_id')
        item_id = self.kwargs.get('item_id')

        if user_id:
            user = User.objects.get(id=user_id)
            cart = Cart.objects.get(id=item_id, cart_id=cart_id, user=user)
        else:
            cart = Cart.objects.get(id=item_id, cart_id=cart_id)

        return cart
    
class CreateOrderAPIView(generics.CreateAPIView):
    serializer_class = CartOrderSerializer
    permission_classes = (AllowAny,)
    queryset = CartOrder.objects.all()
    
    def create(self, request, *args, **kwargs):
        payload = request.data
        full_name = payload.get('full_name')
        email = payload.get('email')
        phone = payload.get('phone')
        country = payload.get('country')
        province = payload.get('province')
        address = payload.get('address')
        user_id = int(payload.get('user_id'))
        cart_id = payload.get('cart_id')
        municipe = payload.get('municipe')
    
        user = User.objects.get(id=user_id) if user_id != 0 else None
        
        cart_items = Cart.objects.filter(cart_id=cart_id)

        total_shipping_amount = Decimal(0.00)
        total_tax_fee = Decimal(0.00)
        total_service_fee = Decimal(0.00)
        total_sub_total = Decimal(0.00)
        total_initial_total = Decimal(0.00)
        total_total = Decimal(0.00)

        order = CartOrder.objects.create(
            buyer=user,
            full_name=full_name,
            email=email,
            phone=phone,
            country=country,
            province=province,
            municipe=municipe or '',
            address=address
        )

        for item in cart_items:
            CartOrderItem.objects.create(
                order=order,
                product=item.product,
                vendor=item.product.vendor,
                quantity=item.quantity,
                price=item.price,
                shipping_amount=item.shipping_amount,
                service_fee=item.service_fee,
                tax_fee=item.tax_fee,
                total=item.total,
                sub_total=item.sub_total,
                initial_total=item.total,
                color=item.color,
                size=item.size,
            )

            total_shipping_amount += Decimal(item.shipping_amount)
            total_tax_fee += Decimal(item.tax_fee)
            total_service_fee += Decimal(item.service_fee)
            total_sub_total += Decimal(item.sub_total)
            total_initial_total += Decimal(item.total)
            total_total += Decimal(item.total)
            order.vendor.add(item.product.vendor)
        
        order.shipping_amount = total_shipping_amount
        order.tax_fee = total_tax_fee
        order.service_fee = total_service_fee
        order.sub_total = total_sub_total
        order.initial_total = total_initial_total
        order.total = total_total
        order.save()

        return Response({"status":"success", "message":"Order Created!", "data":{"order_oid":order.oid}}, status=status.HTTP_201_CREATED)

class CheckoutView(generics.RetrieveAPIView):
    serializer_class = CartOrderSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'order_oid'

    def get_object(self):
        order_oid = self.kwargs.get('order_oid')
        order = CartOrder.objects.get(oid=order_oid)
        return order

class CouponAPIView(generics.ListCreateAPIView):
    serializer_class = CouponSerializer
    permission_classes = (AllowAny,)
    queryset = Coupon.objects.all()

    def create(self, request, *args, **kwargs):
        payload = request.data
        order_oid = payload.get('order_oid')
        coupon_code = payload.get('coupon_code')

        order = CartOrder.objects.get(oid=order_oid)

        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except:
            coupon = None

        if coupon:
            order_items = CartOrderItem.objects.filter(order=order, vendor=coupon.vendor)
            if order_items:
                for item in order_items:
                    if not coupon in item.coupon.all():
                        discount = item.total * Decimal(coupon.discount/100)
                        item.total -= discount
                        item.sub_total -= discount
                        item.coupon.add(coupon)
                        item.saved += discount

                        order.total -= discount
                        order.sub_total -= discount
                        order.saved += discount                        
                        item.save() 
                        order.save() 
                    else:
                        return Response({"status":"info", "message":"Este cupom já foi usado!"}, status=status.HTTP_200_OK)
                return Response({"status":"success", "message":"Cupom activado com sucesso!"}, status=status.HTTP_200_OK)
            else:
                return Response({"status":"info", "message":"Não existem item nesse carrinho!"}, status=status.HTTP_200_OK)
        else:
            return Response({"status":"error", "message":"Este cupom não existe!"}, status=status.HTTP_200_OK)
        

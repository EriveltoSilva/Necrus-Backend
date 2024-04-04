from django.shortcuts import render
from .models import *
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required



def checkout(request):
    return render(request, 'ecommerce/checkout.html')
def contact(request):
    return render(request, 'ecommerce/contact.html')
def detail(request):
    return render(request, 'ecommerce/detail.html')
def shop(request):
    return render(request, 'ecommerce/shop.html')

def wishlist(request):
    return render(request, 'ecommerce/wishlist.html')
def faqs(request):
    return render(request, 'ecommerce/faqs.html')
def about_us(request):
    return render(request, 'ecommerce/about_us.html')


# @login_required(login_url="users:login", redirect_field_name="next")
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_total_price":0, "get_total_items":0}
    return render(request, 'ecommerce/cart.html', {"order":order, "items":items})


@login_required(login_url="users:login", redirect_field_name="next")
def home(request):
    products = Product.objects.all()
    return render(request, 'ecommerce/home.html', {"products":products})
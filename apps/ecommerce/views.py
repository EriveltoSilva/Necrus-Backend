from .models import *
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from django.db.models import Count

def contact(request):
    return render(request, 'ecommerce/contact.html')
def shop(request):
    return render(request, 'ecommerce/shop.html')

def wishlist(request):
    return render(request, 'ecommerce/wishlist.html')
def faqs(request):
    return render(request, 'ecommerce/faqs.html')
def about_us(request):
    return render(request, 'ecommerce/about_us.html')

def detail(request, slug):
    return render(request, 'ecommerce/detail.html')

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_total_price":0, "get_total_items":0}
    return render(request, 'ecommerce/checkout.html',{"order":order, "items":items})

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
    products = Product.objects.filter(is_published=True)
    recent_products = Product.objects.filter(is_published=True)[0:20]
    categories = ProductCategory.objects.filter(is_published=True).annotate(num_products=Count('product'))
    supporters = Supporter.objects.filter(is_published=True)
    carrocels = Carrocel.objects.all()
    context = {
        "categories":categories,
        "products":products, 
        "recent_products":recent_products, 
        "supporters":supporters,
        "carrocels":carrocels
    }
    return render(request, 'ecommerce/home.html', context)
from .models import *
from django.utils import timezone
from django.db.models import Count
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

def contact(request):
    return render(request, 'ecommerce/contact.html')

def wishlist(request):
    return render(request, 'ecommerce/wishlist.html')
def faqs(request):
    return render(request, 'ecommerce/faqs.html')
def about_us(request):
    return render(request, 'ecommerce/about_us.html')



def product_category(request, slug):
    return render(request, 'ecommerce/product-category.html')

# @login_required(login_url="users:login", redirect_field_name="next")
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


@require_POST
def review_create(request):
    if request.user.is_authenticated:
        messages.error(request, "Faça login primeiro para registrar a sua avaliação!")
    product = get_object_or_404(Product, slug=request.POST['slug'])
    Review.objects.create(user=request.user.customer, comment=request.POST['message'], product=product)
    messages.success(request,"Sucesso ao expor a avaliação!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '')


def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_images = product.productimage_set.all()
    recommend_products = Product.objects.filter(is_published=True)
    reviews = Review.objects.filter(is_published=True, product=product)
    num_reviews = reviews.count()
    return render(request, 'ecommerce/detail.html', {"reviews":reviews,"num_reviews":num_reviews ,"product":product, "product_images":product_images, "recommend_products":recommend_products})


def home(request):
    products = Product.objects.filter(is_published=True)
    recent_products = Product.objects.filter(is_published=True)[0:20]
    categories = ProductCategory.objects.filter(is_published=True).annotate(num_products=Count('product'))
    partners = Supporter.objects.filter(is_published=True)
    carrocels = Carrocel.objects.all()
    sales_product = Product.objects.filter(
        is_published=True,  # Ensure products are published
        sale__isnull=False,  # Only consider products with an associated sale
    ).filter(sale__expiration_date__gt=timezone.now())[0:2]
    context = {
        "categories":categories,
        "products":products, 
        "recent_products":recent_products, 
        "partners":partners,
        "carrocels":carrocels,
        "sales_product":sales_product,
    }
    return render(request, 'ecommerce/home.html', context)
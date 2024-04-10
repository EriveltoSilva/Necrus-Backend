import json
import datetime
from .models import *
from django.utils import timezone
from django.db.models import Count
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse

NUM_PRODUCTS = 16

def contact(request):
    order, items = __get_order_and_items(request)
    return render(request, 'ecommerce/contact.html',{"order":order, "items":items, "categories":__get_categories()})

def wishlist(request):
    order, items = __get_order_and_items(request)
    return render(request, 'ecommerce/wishlist.html',{"order":order, "items":items, "categories":__get_categories()})
def faqs(request):
    order, items = __get_order_and_items(request)
    return render(request, 'ecommerce/faqs.html',{"order":order, "items":items, "categories":__get_categories()})
def about_us(request):
    order, items = __get_order_and_items(request)
    return render(request, 'ecommerce/about_us.html',{"order":order, "items":items, "categories":__get_categories()})

def checkout(request):
    order, items = __get_order_and_items(request)

    return render(request, 'ecommerce/checkout.html',{"order":order, "items":items, "categories":__get_categories()})

def cart(request):
    order, items = __get_order_and_items(request)
    return render(request, 'ecommerce/cart.html', {"order":order, "items":items, "categories":__get_categories()})


@require_POST
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order.transaction_id = transaction_id
        order.complete = True
        order.save()

    else:
        print("Usuário não logado")
        return JsonResponse({"status":"sucess", "message":"", "data":[]})
    return JsonResponse({"status":"error", "message": "Usuário não logado no sistema!", "data":[]})


@require_POST
def update_cart_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def product_category(request, slug):
    category = get_object_or_404(ProductCategory, slug=slug)
    list_products = category.product_set.all()
    paginator = Paginator(list_products, NUM_PRODUCTS)
    products = paginator.get_page(request.GET.get('page'))
    order, items = __get_order_and_items(request)
    context={
        "order":order, 
        "items":items, 
        "categories":__get_categories(),
        "category":category,
        "products": products
    }
    return render(request, 'ecommerce/product-category.html', context)




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
    order, items = __get_order_and_items(request)
    context = {
        "order": order,
        "items":items,
        "reviews":reviews,
        "num_reviews":num_reviews ,
        "product":product, 
        "product_images":product_images, 
        "recommend_products":recommend_products,
        "categories":__get_categories(),
    }
    return render(request, 'ecommerce/detail.html', context)


def home(request):
    products = Product.objects.filter(is_published=True)
    recent_products = Product.objects.filter(is_published=True)[0:20]
    partners = Supporter.objects.filter(is_published=True)
    carousels = Carrocel.objects.filter(is_published=True)
    sales_product = Product.objects.filter(
        is_published=True, 
        sale__isnull=False).filter(sale__expiration_date__gt=timezone.now())[0:2]
    order, items = __get_order_and_items(request)

    context = {
        "order":order, 
        "items":items, 
        "categories":__get_categories(),
        "products":products, 
        "recent_products":recent_products, 
        "partners":partners,
        "carrocels":carousels,
        "sales_product":sales_product,
    }
    return render(request, 'ecommerce/home.html', context)








def __get_order_and_items(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.get_cart_items
    else:
        cart = json.loads(request.COOKIES['cart']) if 'cart' in request.COOKIES else {}        
        items = []
        
        order = {"get_total_price":0, "get_total_items":0}
        for item in cart:
            order["get_total_items"] += cart[item]['quantity']
            product = Product.objects.get(id=item)
            order["get_total_price"] += (product.price * cart[item]['quantity'])

        
        
    return (order, items)


def __get_categories():
    return ProductCategory.objects.filter(is_published=True).annotate(num_products=Count('product'))
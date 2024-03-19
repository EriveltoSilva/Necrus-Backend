from django.shortcuts import render

# Create your views here.
def cart(request):
    return render(request, 'ecommerce/cart.html')
def checkout(request):
    return render(request, 'ecommerce/checkout.html')
def contact(request):
    return render(request, 'ecommerce/contact.html')
def detail(request):
    return render(request, 'ecommerce/detail.html')
def home(request):
    return render(request, 'ecommerce/home.html')
def shop(request):
    return render(request, 'ecommerce/shop.html')

def wishlist(request):
    return render(request, 'ecommerce/wishlist.html')
def faqs(request):
    return render(request, 'ecommerce/faqs.html')
def about_us(request):
    return render(request, 'ecommerce/about_us.html')

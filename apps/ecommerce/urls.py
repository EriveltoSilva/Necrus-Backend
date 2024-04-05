from django.urls import path
from . import views

app_name="ecommerce"

urlpatterns = [
    path('', views.home, name="home"),
    path('perguntas-frequentes/', views.faqs, name="faqs"),
    path('sobre-nos/', views.about_us, name="about-us"),

    path('meu-carrinho/', views.cart, name="cart"),
    path('contactos/', views.contact, name="contact"),
    path('produtos/categorias/<int:id>', views.cart, name="product-category"),
    path('produtos/checkout/', views.checkout, name="checkout"),
    path('produtos/detalhes/<slug:slug>/', views.detail, name="detail"),
    path('produtos/comprar/', views.shop, name="shop"),
    path('produtos/minha-lista-de-desejos/', views.wishlist, name="wishlist"),
]
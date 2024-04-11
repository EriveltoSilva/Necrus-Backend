from django.urls import path
from . import views

app_name="ecommerce"

urlpatterns = [
    path('', views.home, name="home"),
    path('perguntas-frequentes/', views.faqs, name="faqs"),
    path('sobre-nos/', views.about_us, name="about-us"),

    path('meu-carrinho/', views.cart, name="cart"),
    path('contactos/', views.contact, name="contact"),
    path('produtos/checkout/', views.checkout, name="checkout"),
    path('produtos/detalhes/<slug:slug>/', views.detail, name="detail"),
    path('produtos/categorias/<slug:slug>/', views.product_category, name="product-category"),
    path('produtos/minha-lista-de-desejos/', views.wishlist, name="wishlist"),
    path('produtos/novos/', views.new_produts_list, name="new-products"),
    path('produtos/destaques/', views.highlights, name="highlights"),


    path('produtos/avaliacoes/', views.review_create, name="review-create"),
    path('produtos/actualizaar-carrinho/', views.update_cart_item, name="update-cart-item"),

]
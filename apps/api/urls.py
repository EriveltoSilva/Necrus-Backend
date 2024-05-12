from . import views
from rest_framework import routers
from django.urls import path, include
from apps.userauths import views as userauths_views
from rest_framework_simplejwt.views import TokenRefreshView
from apps.store import views as store_views
urlpatterns = [
    # User Authentication Endpoints
    path('user/token/', userauths_views.MyTokenObtainPairView.as_view()),    
    path('user/token/refresh', TokenRefreshView.as_view()),    
    path('user/register/', userauths_views.RegisterView.as_view()),    
    path('user/password-reset/<str:email>/', userauths_views.PasswordResetEmailVerifyView.as_view()),    
    path('user/password-change/', userauths_views.PasswordChangeView.as_view(), name="password_change"),    

    # Store Endpoints
    path('categories/', store_views.CategoryListAPIView.as_view()),    
    path('products/', store_views.ProductListAPIView.as_view()),    
    path('products/detail/<slug:slug>/', store_views.ProductDetailAPIView.as_view()),

    # Cart Endpoints
    path('cart/', store_views.CartAPIView.as_view()),    
    path('cart-list/<str:cart_id>/<int:user_id>/', store_views.CartListAPIView.as_view()),
    path('cart-list/<str:cart_id>/', store_views.CartListAPIView.as_view()),
    path('cart-detail/<str:cart_id>/<int:user_id>/', store_views.CartDetailView.as_view()),
    path('cart-detail/<str:cart_id>/', store_views.CartDetailView.as_view()),
    path('cart-delete/<str:cart_id>/<int:item_id>/<int:user_id>/', store_views.CartItemDeleteAPIView.as_view()),
    path('cart-delete/<str:cart_id>/<int:item_id>/', store_views.CartItemDeleteAPIView.as_view()),
    
    path('create-order/', store_views.CreateOrderAPIView.as_view()),

    path('checkout/<str:order_oid>/', store_views.CheckoutView.as_view()),
    path('apply-coupon/', store_views.CouponAPIView.as_view()),

    # Payment Endpoints
    path('stripe-checkout/<uuid:order_oid>/', store_views.StripeCheckoutView.as_view()),

]
from . import views
from rest_framework import routers
from django.urls import path, include

app_name="api"

router = routers.DefaultRouter()

router.register('produtos', views.ProductViewSet, basename='Produtos')
router.register('categorias', views.ProductCategoryViewSet, basename='Categorias')

urlpatterns = [
    path('api/', include(router.urls)),
]
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view =  get_schema_view(
    openapi.Info(
        title="Backend APIs for Necrus E-commerce",
        default_version="v1",
        description="This is a backend of Necrus API",
        terms_of_service="https://necrus.com/policies",
        contact=openapi.Contact(email="eriveltoclenio@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public = True,
    permission_classes = (permissions.AllowAny,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.api.urls')),

    # path('', include('apps.customer.urls')),
    # path('', include('apps.store.urls')),
    # path('', include('apps.userauths.urls')),
    # path('', include('apps.vendor.urls')),
    # path('', include('apps.ecommerce.urls')),


    # Libraries installed
    path('api/vi/docs/', schema_view.with_ui('swagger', cache_timeout=0), name="schema-swagger-ui"),
    path('api-auth/', include('rest_framework.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.contrib import admin
from .models import Vendor
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ['id','name','is_active', 'created_at']
    list_display_links = ['id','name', 'created_at']
    
    prepopulated_fields = {"slug":("name",)}
admin.site.register(Vendor)
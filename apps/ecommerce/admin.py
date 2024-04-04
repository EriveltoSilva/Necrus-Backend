from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
   list_display = ['id', 'user', 'created_at']
   list_display_links = ['id', 'user', 'created_at']
   search_fields = ['user', 'created_at']
   list_per_page = 20

admin.site.register(Customer, CustomerAdmin)


class EmployeeAdmin(admin.ModelAdmin):
   list_display = ['id', 'user', 'created_at']
   list_display_links = ['id', 'user', 'created_at']
   search_fields = ['user', 'created_at']
   list_per_page = 20

admin.site.register(Employee, EmployeeAdmin)

class GenderAdmin(admin.ModelAdmin):
   list_display = ['id', 'name', 'created_at']
   list_display_links = ['id', 'name', 'created_at']
   search_fields = ['name', 'created_at']
   list_per_page = 20

admin.site.register(Gender, GenderAdmin)

class SizeAdmin(admin.ModelAdmin):
   list_display = ['id', 'name', 'created_at']
   list_display_links = ['id', 'name', 'created_at']
   search_fields = ['name', 'created_at']
   list_per_page = 20

admin.site.register(Size, SizeAdmin)

class ColorAdmin(admin.ModelAdmin):
   list_display = ['id', 'name', 'value_hexadecimal', 'created_at']
   list_display_links = ['id', 'name', 'value_hexadecimal', 'created_at']
   search_fields = ['name', 'value_hexadecimal', 'created_at']
   list_per_page = 20

admin.site.register(Color, ColorAdmin)

class SaleAdmin(admin.ModelAdmin):
   list_display = ['id', 'percentage_value','expiration_date', 'created_at']
   list_display_links = ['id','percentage_value', 'expiration_date','created_at']
   search_fields = ['title', 'percentage_value', 'expiration_date', 'created_at']
   list_per_page = 20
   
admin.site.register(Sale, SaleAdmin)
   

class ProductCategoryAdmin(admin.ModelAdmin):
   list_display = ['id', 'name', 'image', 'created_at']
   list_display_links = ['id', 'name', 'created_at']
   search_fields = ['name', 'description', 'created_at']
   list_per_page = 20

admin.site.register(ProductCategory, ProductCategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
   list_display = ['id','name', 'price', 'created_at']
   list_display_links = ['id','name', 'price', 'created_at']
   search_fields = ['name', 'price', 'created_at']
   list_per_page = 20

admin.site.register(Product,ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
   list_display = ['id','customer', 'complete','transaction_id', 'created_at']
   list_display_links = ['id','customer','transaction_id', 'created_at']
   list_per_page = 20

admin.site.register(Order,OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
   list_display = ['id','product', 'order','quantity', 'created_at']
   list_display_links = ['id','product', 'order','quantity', 'created_at']
   list_per_page = 20
    
admin.site.register(OrderItem,OrderItemAdmin)

class ShippingAddressAdmin(admin.ModelAdmin):
   list_display = ['id','customer', 'order','address', 'created_at']
   list_display_links = ['id','customer', 'order','address', 'created_at']
   list_per_page = 20

admin.site.register(ShippingAddress, ShippingAddressAdmin)
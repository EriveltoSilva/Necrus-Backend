from django.contrib import admin
from .models import Customer, Product, Order, OrderItem, ShippingAddress
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
   list_display = ['id','user','name', 'email', 'created_at']
   list_display_links = ['id','user','name', 'email', 'created_at']
    
class ProductAdmin(admin.ModelAdmin):
   list_display = ['id','name', 'price', 'created_at']
   list_display_links = ['id','name', 'price', 'created_at']

class OrderAdmin(admin.ModelAdmin):
   list_display = ['id','customer', 'complete','transaction_id', 'created_at']
   list_display_links = ['id','customer','transaction_id', 'created_at']

class OrderItemAdmin(admin.ModelAdmin):
   list_display = ['id','product', 'order','quantity', 'created_at']
   list_display_links = ['id','product', 'order','quantity', 'created_at']
    
class ShippingAddressAdmin(admin.ModelAdmin):
   list_display = ['id','customer', 'order','address', 'created_at']
   list_display_links = ['id','customer', 'order','address', 'created_at']

admin.site.register(Customer,CustomerAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order,OrderAdmin )
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
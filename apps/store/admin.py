from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
   list_display = ['id', 'title', 'image', 'created_at']
   list_display_links = ['id', 'title', 'created_at']
   search_fields = ['title', 'description', 'created_at']
   list_per_page = 20
   prepopulated_fields = {"slug":("title",)}
admin.site.register(Category, CategoryAdmin)



class ProductAdmin(admin.ModelAdmin):
   list_display = ['id','title', 'price', 'created_at']
   list_display_links = ['id','title', 'price', 'created_at']
   search_fields = ['title', 'price', 'created_at']
   list_per_page = 20
   prepopulated_fields = {"slug":("title",)}
admin.site.register(Product,ProductAdmin)
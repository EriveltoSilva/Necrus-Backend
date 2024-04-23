from django.contrib import admin
from .models import Category, Product, Gallery, Specification, Size, Color


class GalleryAdminInline(admin.TabularInline):
   model = Gallery
   extra = 0
   
class SpecificationAdminInline(admin.TabularInline):
   model = Specification
   extra = 0

class SizeAdminInline(admin.TabularInline):
   model = Size
   extra = 0

class ColorAdminInline(admin.TabularInline):
   model = Color
   extra = 0


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
   inlines = [GalleryAdminInline, SpecificationAdminInline, SizeAdminInline, ColorAdminInline]
admin.site.register(Product,ProductAdmin)
from django.contrib import admin
from .models import *

# class GenderAdmin(admin.ModelAdmin):
#    list_display = ['id','is_published', 'name', 'created_at']
#    list_display_links = ['id', 'name', 'created_at']
#    search_fields = ['name', 'created_at']
#    list_editable = ['is_published']
#    list_per_page = 20
# admin.site.register(Gender, GenderAdmin)

# class SizeAdmin(admin.ModelAdmin):
#    list_display = ['id','is_published', 'name', 'created_at']
#    list_display_links = ['id', 'name', 'created_at']
#    search_fields = ['name', 'created_at']
#    list_editable = ['is_published']
#    list_per_page = 20
# admin.site.register(Size, SizeAdmin)

# class ColorAdmin(admin.ModelAdmin):
#    list_display = ['id','is_published', 'name', 'value_hexadecimal', 'created_at']
#    list_display_links = ['id', 'name', 'value_hexadecimal', 'created_at']
#    search_fields = ['name', 'value_hexadecimal', 'created_at']
#    list_editable = ['is_published']
#    list_per_page = 20
# admin.site.register(Color, ColorAdmin)

# class SaleAdmin(admin.ModelAdmin):
#    list_display = ['id','name','is_published', 'percentage_value','expiration_date', 'created_at']
#    list_display_links = ['id','name','percentage_value', 'expiration_date','created_at']
#    search_fields = ['name', 'percentage_value', 'expiration_date', 'created_at']
#    list_editable = ['is_published']
#    list_per_page = 20
# admin.site.register(Sale, SaleAdmin)
   

class ProductCategoryAdmin(admin.ModelAdmin):
   list_display = ['id', 'title','is_published', 'image', 'created_at']
   list_display_links = ['id', 'title', 'created_at']
   search_fields = ['title', 'description', 'created_at']
   list_editable = ['is_published']
   list_per_page = 20
   prepopulated_fields = {"slug":("title",)}
admin.site.register(ProductCategory, ProductCategoryAdmin)

class ProductImageAdmin(admin.TabularInline):
   model = ProductImage
   # list_display = ['id','product', 'created_at']
   # list_display_links = ['id','product', 'created_at']
   # search_fields = ['created_at']
   # list_per_page = 20
# admin.site.register(ProductImage, ProductImageAdmin)

class ProductAdmin(admin.ModelAdmin):
   inlines = [ProductImageAdmin]

   list_display = ['id','title','is_published', 'price', 'created_at']
   list_display_links = ['id','title', 'price', 'created_at']
   search_fields = ['title', 'price', 'created_at']
   list_editable = ['is_published']
   list_per_page = 20
   prepopulated_fields = {"slug":("title",)}
admin.site.register(Product,ProductAdmin)





class OrderAdmin(admin.ModelAdmin):
   list_display = ['id','user', 'complete','transaction_id', 'created_at']
   list_display_links = ['id','user','transaction_id', 'created_at']
   list_per_page = 20
admin.site.register(Order,OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
   list_display = ['id','product', 'order','quantity', 'created_at']
   list_display_links = ['id','product', 'order','quantity', 'created_at']
   list_per_page = 20
admin.site.register(OrderItem,OrderItemAdmin)

class ProductReviewAdmin(admin.ModelAdmin):
   list_display = ['id','user','rating', 'product', 'is_published', 'created_at']
   list_display_links = ['id','user','rating', 'product', 'created_at']
   list_per_page = 20
admin.site.register(ProductReview,ProductReviewAdmin)

class WishlistAdmin(admin.ModelAdmin):
   list_display = ['id','user', 'product', 'created_at']
   list_display_links = ['id','user', 'product', 'created_at']
   list_per_page = 20
admin.site.register(Wishlist,WishlistAdmin)

class AddressAdmin(admin.ModelAdmin):
   list_display = ['id','user','address', 'created_at']
   list_display_links = ['id','user','address', 'created_at']
   list_per_page = 20
admin.site.register(Address, AddressAdmin)

class PartnerAdmin(admin.ModelAdmin):
   list_display = ['id', 'name','email' ,'created_at']
   list_display_links = ['id', 'name','email', 'created_at']
   search_fields = ['name','email', 'created_at']
   list_per_page = 20
admin.site.register(Partner, PartnerAdmin)

class CarouselAdmin(admin.ModelAdmin):
   list_display = ['id','title', 'is_published', 'created_at']
   list_display_links = ['id','title', 'is_published', 'created_at']
   search_fields = ['title', 'is_published', 'created_at']
   list_per_page = 20
admin.site.register(Carousel, CarouselAdmin)


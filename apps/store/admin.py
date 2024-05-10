from django.contrib import admin
from .models import Category, Product, Gallery, Specification, Size, Color, Cart, CartOrder, CartOrderItem
from .models import ProductFaq, Review, Wishlist,Notification, Coupon, Tax


class TaxAdmin(admin.ModelAdmin):
   list_display = ['id', 'country', 'rate', 'created_at']
   list_display_links = ['id', 'country', 'rate', 'created_at']
   list_per_page = 20
admin.site.register(Tax, TaxAdmin)

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



class CartAdmin(admin.ModelAdmin):
   list_display = ['id', 'product', 'quantity','total', 'created_at']
   list_display_links = ['id', 'product', 'quantity','total', 'created_at']
   search_fields = ['product', 'quantity','created_at']
   list_per_page = 20
admin.site.register(Cart)


class CartOrderAdmin(admin.ModelAdmin):
   list_display = ['oid','buyer', 'sub_total','total', 'payment_status', 'order_status', 'province']
   list_display_links = ['buyer', 'sub_total','total', 'payment_status', 'order_status', 'province']
   search_fields = ['oid','buyer', 'payment_status','order_status','country' ,'province', 'municipe', 'address']
   list_per_page = 20
admin.site.register(CartOrder,CartOrderAdmin)


class CartOrderItemAdmin(admin.ModelAdmin):
   list_display = ['order', 'product', 'vendor', 'quantity','sub_total', 'total']
   list_display_links = ['order', 'product', 'vendor', 'quantity','sub_total', 'total']
   search_fields = ['order', 'quantity', 'sub_total', 'total']
   list_per_page = 20
admin.site.register(CartOrderItem,CartOrderItemAdmin)


class ProductFaqAdmin(admin.ModelAdmin):
   list_display = ['user', 'product', 'is_active']
   list_display_links = ['user', 'product', 'is_active']
   search_fields = ['user', 'product', 'question', 'answer']
   list_filter = ['user','product','is_active', 'created_at']
   list_per_page = 20
admin.site.register(ProductFaq,ProductFaqAdmin)

class ReviewAdmin(admin.ModelAdmin):
   list_display = ['user', 'product', 'rating', 'is_active','created_at']
   list_display_links = ['user', 'product', 'rating', 'created_at']
   search_fields = [ 'user','review', 'reply']
   list_filter = ['user', 'product', 'is_active']
   list_per_page = 20
admin.site.register(Review, ReviewAdmin)

class WishlistAdmin(admin.ModelAdmin):
   list_display = ['user', 'product', 'created_at']
   list_display_links = ['user', 'product', 'created_at']
   search_fields = ['user', 'created_at']
   list_filter = ['user', 'product', 'created_at']
   list_per_page = 20
admin.site.register(Wishlist, WishlistAdmin)

class NotificationAdmin(admin.ModelAdmin):
   list_display = ['user', 'vendor', 'order','order_item', 'seen', 'created_at']
   list_display_links = ['user', 'vendor', 'order','order_item', 'seen', 'created_at']
   search_fields = ['user', 'vendor',  'order_item']
   list_filter = ['user', 'vendor', 'order_item', 'seen', 'created_at']
   list_per_page = 20
admin.site.register(Notification,NotificationAdmin)

class CouponAdmin(admin.ModelAdmin):
   list_display = ['vendor', 'code', 'discount','created_at']
   list_display_links = ['vendor', 'code', 'discount']
   search_fields = ['vendor',  'code', 'discount']
   list_filter = ['code', 'vendor']
   list_per_page = 20
admin.site.register(Coupon,CouponAdmin)



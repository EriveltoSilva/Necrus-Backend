from django.contrib import admin
from .models import User, Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'username','email', 'phone']
    list_display_links = ['id', 'full_name', 'username','email', 'phone']
    search_fields = ['full_name', 'username','email']
    list_per_page = 20
admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'gender','country','created_at']
    list_display_links = ['full_name', 'gender','country','created_at']
    search_fields = ['full_name', 'country',]
    list_filter = ['gender', 'created_at']
    list_per_page = 20
admin.site.register(Profile, ProfileAdmin)
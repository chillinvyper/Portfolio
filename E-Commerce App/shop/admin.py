from django.contrib import admin
from .models import UserProfile, Store, Product

# Register your models here.

# using the decorator approach to register my admin models
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    '''registering admin for the User model'''
    list_display = ('user', 'role')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')

    # creating the search fields, using name and the API "follow" on owner username
    # "follow" notation uses a parent category to narrow down search to find model
    search_fields = ('name', 'owner__username')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'price', 'stock')
    list_filter = ['store']
    search_fields = ('name', 'store__name')

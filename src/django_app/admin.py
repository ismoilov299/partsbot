"""
Django admin configuration
"""
from django.contrib import admin
from .models import User, City, CarBrand, Shop, UstaXona, Request


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'first_name', 'last_name', 'username', 'language', 'is_active', 'created_at']
    list_filter = ['language', 'is_active', 'created_at']
    search_fields = ['telegram_id', 'username', 'first_name', 'last_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'name_ru', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name_uz', 'name_ru']


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'name_ru', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name_uz', 'name_ru']
    ordering = ['order', 'name_uz']


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'city', 'phone', 'is_approved', 'is_active', 'created_at']
    list_filter = ['is_approved', 'is_active', 'city', 'created_at']
    search_fields = ['name', 'phone', 'address', 'owner__first_name']
    filter_horizontal = ['car_brands']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'car_brand', 'city', 'status', 'created_at']
    list_filter = ['status', 'car_brand', 'city', 'created_at']
    search_fields = ['description', 'phone', 'user__first_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UstaXona)
class UstaXonaAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'city', 'phone', 'is_approved', 'is_active', 'created_at']
    list_filter = ['is_approved', 'is_active', 'city', 'created_at']
    search_fields = ['name', 'phone', 'address', 'owner__first_name']
    filter_horizontal = ['car_brands']
    readonly_fields = ['created_at', 'updated_at']

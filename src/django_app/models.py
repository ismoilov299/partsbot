"""
Django models for the bot
"""
from django.db import models


class User(models.Model):
    """User model to store telegram user information"""
    telegram_id = models.BigIntegerField(unique=True, db_index=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=10, default='uz', choices=[
        ('uz', 'O\'zbekcha'),
        ('ru', 'Русский'),
    ])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.telegram_id} - {self.first_name}"


class City(models.Model):
    """City model"""
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cities'
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return f"{self.name_uz} / {self.name_ru}"


class CarBrand(models.Model):
    """Car brand model"""
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'car_brands'
        ordering = ['order', 'name_uz']
        verbose_name = 'Car Brand'
        verbose_name_plural = 'Car Brands'

    def __str__(self):
        return f"{self.name_uz} / {self.name_ru}"


class Shop(models.Model):
    """Shop model"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='shops')
    car_brands = models.ManyToManyField(CarBrand, related_name='shops')
    phone = models.CharField(max_length=20)
    address = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True, help_text='Shop latitude')
    longitude = models.FloatField(null=True, blank=True, help_text='Shop longitude')
    photo_path = models.CharField(max_length=500, null=True, blank=True, help_text='Local path to shop photo file')
    description = models.TextField(null=True, blank=True)
    part_categories_uz = models.JSONField(null=True, blank=True, help_text='Part categories in Uzbek')
    part_categories_ru = models.JSONField(null=True, blank=True, help_text='Part categories in Russian')
    is_approved = models.BooleanField(default=False, help_text='Admin approved')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shops'
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'

    def __str__(self):
        return f"{self.name} - {self.city.name_uz}"


class UstaXona(models.Model):
    """Usta Xona (Service Center) model"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usta_xonalar')
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='usta_xonalar')
    car_brands = models.ManyToManyField(CarBrand, related_name='usta_xonalar')
    phone = models.CharField(max_length=20)
    address = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True, help_text='Service center latitude')
    longitude = models.FloatField(null=True, blank=True, help_text='Service center longitude')
    photo_path = models.CharField(max_length=500, null=True, blank=True, help_text='Local path to service center photo file')
    description = models.TextField(null=True, blank=True)
    service_types_uz = models.JSONField(null=True, blank=True, help_text='Service types in Uzbek')
    service_types_ru = models.JSONField(null=True, blank=True, help_text='Service types in Russian')
    is_approved = models.BooleanField(default=False, help_text='Admin approved')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'usta_xonalar'
        verbose_name = 'Usta Xona'
        verbose_name_plural = 'Usta Xonalar'

    def __str__(self):
        return f"{self.name} - {self.city.name_uz}"


class Request(models.Model):
    """User request model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    car_brand = models.ForeignKey(CarBrand, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'requests'
        ordering = ['-created_at']
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'

    def __str__(self):
        return f"Request #{self.id} - {self.user.first_name}"

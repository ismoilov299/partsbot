"""
Database utilities for bot
"""
import os
import sys
import django
from typing import Optional, List

# Add the project root to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.django_app.settings')
django.setup()

from src.django_app.models import User, City, CarBrand, Shop, UstaXona, Request
from asgiref.sync import sync_to_async


class DatabaseManager:
    """Database operations manager"""
    
    @staticmethod
    @sync_to_async
    def get_or_create_user(telegram_id: int, username: str = None, 
                          first_name: str = None, last_name: str = None) -> User:
        """Get or create a user"""
        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
            }
        )
        if not created:
            # Update user info if changed
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        return user
    
    @staticmethod
    @sync_to_async
    def update_user_language(telegram_id: int, language: str) -> None:
        """Update user's language preference"""
        User.objects.filter(telegram_id=telegram_id).update(language=language)
    
    @staticmethod
    @sync_to_async
    def get_user(telegram_id: int) -> Optional[User]:
        """Get user by telegram_id"""
        try:
            return User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    @sync_to_async
    def get_all_cities() -> List[City]:
        """Get all active cities"""
        return list(City.objects.filter(is_active=True).order_by('name_uz'))
    
    @staticmethod
    @sync_to_async
    def get_city(city_id: int) -> Optional[City]:
        """Get city by id"""
        try:
            return City.objects.get(id=city_id, is_active=True)
        except City.DoesNotExist:
            return None
    
    @staticmethod
    @sync_to_async
    def get_car_brand_by_order(order: int) -> Optional[CarBrand]:
        """Get car brand by order number (1-7)"""
        try:
            brands = list(CarBrand.objects.filter(is_active=True).order_by('order', 'name'))
            if 0 < order <= len(brands):
                return brands[order - 1]
            return None
        except Exception:
            return None
    
    @staticmethod
    @sync_to_async
    def search_shops(city_id: int, car_brand_id: int = None) -> List[Shop]:
        """Search shops by city and optionally by car brand"""
        query = Shop.objects.filter(city_id=city_id, is_active=True, is_approved=True)
        if car_brand_id:
            query = query.filter(car_brands__id=car_brand_id)
        return list(query.select_related('city', 'owner').prefetch_related('car_brands'))
    
    @staticmethod
    @sync_to_async
    def search_usta_xonalar(city_id: int, car_brand_id: int = None) -> List[UstaXona]:
        """Search usta xonalar by city and optionally by car brand"""
        query = UstaXona.objects.filter(city_id=city_id, is_active=True, is_approved=True)
        if car_brand_id:
            query = query.filter(car_brands__id=car_brand_id)
        return list(query.select_related('city', 'owner').prefetch_related('car_brands'))
    
    @staticmethod
    @sync_to_async
    def create_shop(owner_id: int, name: str, city_id: int, 
                   phone: str, address: str = None, 
                   description: str = None, car_brand_ids: List[int] = None,
                   photo_file_id: str = None, latitude: float = None,
                   longitude: float = None, part_categories_uz: List[str] = None,
                   part_categories_ru: List[str] = None) -> Shop:
        """Create a new shop"""
        owner = User.objects.get(telegram_id=owner_id)
        shop = Shop.objects.create(
            owner=owner,
            name=name,
            city_id=city_id,
            phone=phone,
            address=address,
            description=description,
            photo_file_id=photo_file_id,
            latitude=latitude,
            longitude=longitude,
            part_categories_uz=part_categories_uz,
            part_categories_ru=part_categories_ru
        )
        if car_brand_ids:
            shop.car_brands.set(car_brand_ids)
        return shop
    
    @staticmethod
    @sync_to_async
    def create_request(user_id: int, description: str, 
                      car_brand_id: int = None, city_id: int = None, 
                      phone: str = None) -> Request:
        """Create a new request"""
        user = User.objects.get(telegram_id=user_id)
        request = Request.objects.create(
            user=user,
            description=description,
            car_brand_id=car_brand_id,
            city_id=city_id,
            phone=phone
        )
        return request
    
    @staticmethod
    @sync_to_async
    def get_all_car_brands() -> List[CarBrand]:
        """Get all active car brands"""
        return list(CarBrand.objects.filter(is_active=True).order_by('order', 'name_uz'))
    
    @staticmethod
    @sync_to_async
    def get_car_brand(brand_id: int) -> Optional[CarBrand]:
        """Get car brand by id"""
        try:
            return CarBrand.objects.get(id=brand_id, is_active=True)
        except CarBrand.DoesNotExist:
            return None
    
    @staticmethod
    @sync_to_async
    def get_shop_by_id(shop_id: int) -> Optional[Shop]:
        """Get shop by ID"""
        try:
            return Shop.objects.select_related('city', 'owner').prefetch_related('car_brands').get(id=shop_id)
        except Shop.DoesNotExist:
            return None
    
    @staticmethod
    @sync_to_async
    def approve_shop(shop_id: int) -> bool:
        """Approve shop"""
        try:
            Shop.objects.filter(id=shop_id).update(is_approved=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    @sync_to_async
    def reject_shop(shop_id: int) -> bool:
        """Reject and delete shop"""
        try:
            Shop.objects.filter(id=shop_id).delete()
            return True
        except Exception:
            return False


# Global instance
db = DatabaseManager()

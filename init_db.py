"""
Database initialization script
Creates initial data: cities and car brands
"""
import os
import sys
import django

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.django_app.settings')
django.setup()

from django_app.models import City, CarBrand


def init_cities():
    """Initialize cities"""
    cities_data = [
        {'name_uz': 'Toshkent', 'name_ru': 'Ташкент'},
        {'name_uz': 'Andijon', 'name_ru': 'Андижан'},
        {'name_uz': 'Buxoro', 'name_ru': 'Бухара'},
        {'name_uz': 'Farg\'ona', 'name_ru': 'Фергана'},
        {'name_uz': 'Jizzax', 'name_ru': 'Джизак'},
        {'name_uz': 'Namangan', 'name_ru': 'Наманган'},
        {'name_uz': 'Navoiy', 'name_ru': 'Навои'},
        {'name_uz': 'Qashqadaryo', 'name_ru': 'Кашкадарья'},
        {'name_uz': 'Qoraqalpog\'iston', 'name_ru': 'Каракалпакстан'},
        {'name_uz': 'Samarqand', 'name_ru': 'Самарканд'},
        {'name_uz': 'Sirdaryo', 'name_ru': 'Сырдарья'},
        {'name_uz': 'Surxondaryo', 'name_ru': 'Сурхандарья'},
        {'name_uz': 'Toshkent viloyati', 'name_ru': 'Ташкентская область'},
        {'name_uz': 'Xorazm', 'name_ru': 'Хорезм'},
    ]
    
    for city_data in cities_data:
        city, created = City.objects.get_or_create(
            name_uz=city_data['name_uz'],
            defaults={'name_ru': city_data['name_ru']}
        )
        if created:
            print(f"Created city: {city.name_uz}")
        else:
            print(f"City already exists: {city.name_uz}")


def init_car_brands():
    """Initialize car brands"""
    brands_data = [
        {'name_uz': 'KIA/HYUNDAI', 'name_ru': 'KIA/HYUNDAI', 'order': 1},
        {'name_uz': 'CHEVROLET GM', 'name_ru': 'CHEVROLET GM', 'order': 2},
        {'name_uz': 'CHERY/JETOUR/HAVAL', 'name_ru': 'CHERY/JETOUR/HAVAL', 'order': 3},
        {'name_uz': 'BYD', 'name_ru': 'BYD', 'order': 4},
        {'name_uz': 'BMW', 'name_ru': 'BMW', 'order': 5},
        {'name_uz': 'MERCEDES BENZ', 'name_ru': 'MERCEDES BENZ', 'order': 6},
        {'name_uz': 'Boshqa Inomarkalar', 'name_ru': 'Другие Иномарки', 'order': 7},
        {'name_uz': 'Barchasi', 'name_ru': 'Все', 'order': 0},
    ]
    
    for brand_data in brands_data:
        brand, created = CarBrand.objects.get_or_create(
            name_uz=brand_data['name_uz'],
            defaults={'name_ru': brand_data['name_ru'], 'order': brand_data['order']}
        )
        if created:
            print(f"Created car brand: {brand.name_uz}")
        else:
            print(f"Car brand already exists: {brand.name_uz}")


if __name__ == '__main__':
    print("Initializing database...")
    print("\n=== Creating cities ===")
    init_cities()
    print("\n=== Creating car brands ===")
    init_car_brands()
    print("\n✅ Database initialization complete!")

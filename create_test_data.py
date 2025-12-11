"""
Test data script - adds sample shops for testing
"""
import os
import sys
import django

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')
django.setup()

from django_app.models import User, City, CarBrand, Shop


def create_test_data():
    """Create test shops and users"""
    
    # Create test user
    test_user, created = User.objects.get_or_create(
        telegram_id=123456789,
        defaults={
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'language': 'uz'
        }
    )
    
    if created:
        print(f"Created test user: {test_user.first_name}")
    
    # Get cities
    tashkent = City.objects.get(name_uz='Toshkent')
    samarkand = City.objects.get(name_uz='Samarqand')
    
    # Get car brands
    kia = CarBrand.objects.get(name='KIA/HYUNDAI')
    chevrolet = CarBrand.objects.get(name='CHEVROLET GM')
    bmw = CarBrand.objects.get(name='BMW')
    
    # Create test shops
    shops_data = [
        {
            'name': "Avtoehtiyot do'koni",
            'city': tashkent,
            'brands': [kia, chevrolet],
            'phone': '+998901234567',
            'address': 'Chilonzor, 12-kvartal',
            'description': 'KIA va Chevrolet uchun orginal va analogli ehtiyot qismlar'
        },
        {
            'name': 'BMW Parts Center',
            'city': tashkent,
            'brands': [bmw],
            'phone': '+998907654321',
            'address': 'Yunusobod, Amir Temur ko\'chasi',
            'description': 'BMW uchun orginal ehtiyot qismlar'
        },
        {
            'name': "Samarqand Auto Parts",
            'city': samarkand,
            'brands': [kia, chevrolet],
            'phone': '+998662345678',
            'address': 'Registon maydon yaqini',
            'description': 'Barcha ehtiyot qismlar'
        }
    ]
    
    for shop_data in shops_data:
        brands = shop_data.pop('brands')
        shop, created = Shop.objects.get_or_create(
            name=shop_data['name'],
            defaults={
                **shop_data,
                'owner': test_user
            }
        )
        
        if created:
            shop.car_brands.set(brands)
            print(f"✅ Created shop: {shop.name} in {shop.city.name_uz}")
        else:
            print(f"Shop already exists: {shop.name}")


if __name__ == '__main__':
    print("Creating test data...")
    print()
    create_test_data()
    print()
    print("✅ Test data created successfully!")
    print("\nYou can now test the bot:")
    print("1. Start Redis: .\\start_redis.ps1")
    print("2. Start bot: .\\start_bot.ps1")
    print("3. Send /start to your bot")

import os
import sys
import django

project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.django_app.settings')
django.setup()

from src.django_app.models import UstaXona, City, CarBrand, User

# Get or create test user
user, _ = User.objects.get_or_create(
    telegram_id=1161180912,
    defaults={'username': 'test', 'first_name': 'Test'}
)

# Get city
city = City.objects.get(id=1)  # Toshkent

# Create usta xona
usta = UstaXona.objects.create(
    owner=user,
    name="Test Usta Xona",
    city=city,
    phone="+998901234567",
    address="Toshkent, Chilonzor",
    description="Test usta xona",
    is_approved=True,
    is_active=True
)

# Add brands
brands = CarBrand.objects.filter(id__in=[8, 2, 3])  # KIA, CHEVROLET, CHERY
usta.car_brands.set(brands)

print(f"✅ Test usta xona yaratildi: ID={usta.id}")
print(f"   Nomi: {usta.name}")
print(f"   Shahar: {usta.city.name_uz}")
print(f"   Markalar: {[b.name_uz for b in usta.car_brands.all()]}")

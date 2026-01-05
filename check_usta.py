import os
import sys
import django

project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.django_app.settings')
django.setup()

from src.django_app.models import UstaXona, City, CarBrand

print("\n" + "="*60)
print("USTA XONALAR DATABASE CHECK")
print("="*60)

# Get all usta xonalar
usta_xonalar = UstaXona.objects.all()
print(f"\nJami usta xonalar: {usta_xonalar.count()}\n")

if usta_xonalar.count() == 0:
    print("WARNING: Database bosh - hech qanday usta xona yoq!\n")
else:
    for ux in usta_xonalar:
        brands = list(ux.car_brands.all())
        brand_names = [b.name_uz for b in brands]
        brand_ids = [b.id for b in brands]
        
        print(f"{'─'*60}")
        print(f"ID: {ux.id}")
        print(f"Nomi: {ux.name}")
        print(f"Shahar: {ux.city.name_uz} (ID: {ux.city.id})")
        print(f"Telefon: {ux.phone}")
        print(f"Manzil: {ux.address or 'N/A'}")
        approved_status = '✅ HA' if ux.is_approved else '❌ YOQ'
        active_status = '✅ HA' if ux.is_active else '❌ YOQ'
        print(f"Tasdiqlangan (is_approved): {approved_status}")
        print(f"Faol (is_active): {active_status}")
        print(f"Markalar: {', '.join(brand_names) if brand_names else 'BOGLANMAGAN'}")
        print(f"Marka IDs: {brand_ids}")
        has_photo = '✅ Bor' if ux.photo_file_id else '❌ Yoq'
        has_location = '✅ Bor' if ux.latitude else '❌ Yoq'
        print(f"Rasm: {has_photo}")
        print(f"Lokatsiya: {has_location}")

print("\n" + "="*60)
print("QIDIRUV PARAMETRLARI BILAN TEKSHIRISH")
print("="*60)

# Check search params from log
brand_id = 8
city_id = 1

print(f"\nQidiruv parametrlari:")
print(f"  - Brand ID: {brand_id}")
print(f"  - City ID: {city_id}")

try:
    city = City.objects.get(id=city_id)
    print(f"  - Shahar: {city.name_uz}")
except City.DoesNotExist:
    print(f"  - WARNING: Shahar topilmadi!")

try:
    brand = CarBrand.objects.get(id=brand_id)
    print(f"  - Marka: {brand.name_uz}")
except CarBrand.DoesNotExist:
    print(f"  - WARNING: Marka topilmadi!")

# Search with exact params
results = UstaXona.objects.filter(city_id=city_id, is_active=True, is_approved=True)
print(f"\nCity va status bo'yicha: {results.count()} ta")

results_with_brand = results.filter(car_brands__id=brand_id)
print(f"Marka qo'shilganda: {results_with_brand.count()} ta")

# Show all with this city but without filtering by approval
all_in_city = UstaXona.objects.filter(city_id=city_id)
print(f"\nShahar bo'yicha BARCHASI (tasdiqlangan/tasdiqlanmagan): {all_in_city.count()} ta")

for ux in all_in_city:
    status = "OK" if ux.is_approved else "NO"
    active = "OK" if ux.is_active else "NO"
    brands = [b.id for b in ux.car_brands.all()]
    has_brand = "YES" if brand_id in brands else "NO"
    print(f"  {status} Approved | {active} Active | {has_brand} Brand {brand_id} | {ux.name}")

print("\n" + "="*60)


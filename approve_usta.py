import os
import sys
import django

project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.django_app.settings')
django.setup()

from src.django_app.models import UstaXona

# Approve all usta xonalar
usta_xonalar = UstaXona.objects.filter(is_approved=False)
count = usta_xonalar.count()

print(f"\nTasdiqlash kerak bo'lgan usta xonalar: {count}\n")

for ux in usta_xonalar:
    ux.is_approved = True
    ux.save()
    brands = [b.name_uz for b in ux.car_brands.all()]
    print(f"✅ Tasdiqlandi: {ux.name} - {ux.city.name_uz} - Markalar: {brands}")

print(f"\n✅ Jami {count} ta usta xona tasdiqlandi!\n")

import os
import sys
import django

project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.django_app.settings')
django.setup()

from src.django_app.models import UstaXona

usta_xonalar = UstaXona.objects.all()
print(f"\nJami usta xonalar: {usta_xonalar.count()}\n")

for ux in usta_xonalar:
    brands = list(ux.car_brands.values_list('name_uz', flat=True))
    print(f"ID: {ux.id}")
    print(f"Nomi: {ux.name}")
    print(f"Shahar: {ux.city.name_uz}")
    print(f"Tasdiqlangan: {ux.is_approved}")
    print(f"Faol: {ux.is_active}")
    print(f"Markalar: {brands}")
    print("-" * 50)

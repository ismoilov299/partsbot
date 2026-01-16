"""
Script to check Django superuser status
Run this with: python manage.py shell < check_user.py
Or copy-paste these commands one by one in Django shell
"""

from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.filter(is_superuser=True).first()

if user:
    print(f"Username: {user.username}")
    print(f"is_staff: {user.is_staff}")
    print(f"is_active: {user.is_active}")
    print(f"is_superuser: {user.is_superuser}")
    
    # Fix if needed
    if not user.is_staff or not user.is_active:
        print("\n⚠️ User is not staff or not active! Fixing...")
        user.is_staff = True
        user.is_active = True
        user.save()
        print("✅ Fixed! User is now staff and active.")
else:
    print("❌ No superuser found!")
    print("\nTo create a superuser, run:")
    print("python manage.py createsuperuser")


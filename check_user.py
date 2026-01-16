"""
Script to check Django superuser status and change password
Run this with: python manage.py shell < check_user.py
Or copy-paste these commands one by one in Django shell (WITHOUT indentation)
"""

from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='admin')

# Change password
user.set_password('Admin123!@#')
user.save()
print("✅ Password changed to: Admin123!@#")

# Verify
print(f"Username: {user.username}")
print(f"is_staff: {user.is_staff}")
print(f"is_active: {user.is_active}")
print(f"is_superuser: {user.is_superuser}")


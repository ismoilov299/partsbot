"""
WSGI config for django_app project.
"""
import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Add project root to path
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.django_app.settings')

application = get_wsgi_application()

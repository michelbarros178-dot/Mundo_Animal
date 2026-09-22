# create_superuser.py
"""
Crea el superusuario automáticamente si no existe.
Se ejecuta al arrancar el contenedor en Render.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mundo_animal_web.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@admin.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Admin123!')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"✅ Superusuario '{username}' creado exitosamente.")
else:
    print(f"ℹ️ El superusuario '{username}' ya existe. No se creó de nuevo.")
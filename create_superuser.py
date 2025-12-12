#!/usr/bin/env python
"""
Script para crear superusuario automáticamente si no existe
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'admin'
email = 'admin@systemcitas.com'
password = 'admin123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        rol='admin'
    )
    print(f'✅ Superusuario "{username}" creado exitosamente')
else:
    print(f'ℹ️  Superusuario "{username}" ya existe')

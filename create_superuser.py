# create_superuser.py

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')  # Замени 'mysite' на имя твоего проекта, если другое

import django
django.setup()

from django.contrib.auth.models import User

# Проверяем, существует ли уже superuser с логином 'admin'
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',   # Логин
        email='admin@example.com',  # Email (можно любой или пустой '')
        password='123456'   # Пароль — обязательно запомни или измени на свой
    )
    print("Superuser 'admin' успешно создан!")
    print("Логин: admin")
    print("Пароль: 123456")
else:
    print("Superuser 'admin' уже существует.")
# Запусти это в Django shell:
# docker compose exec web python manage.py shell

from django.contrib.auth.models import User, Group
from core.models import Staff
from django.utils import timezone

# Параметры нового пользователя (измени на нужные)
login = "tech1"            # Логин
password = "12345"         # Пароль (лучше потом сменить через админку)
fio = "Сидоров Алексей Петрович"   # ФИО
email = "tech1@company.ru"         # Email (можно оставить пустым "")

# 1. Создаём пользователя
if User.objects.filter(username=login).exists():
    print(f"Пользователь с логином {login} уже существует!")
else:
    user = User.objects.create_user(
        username=login,
        password=password,
        email=email,
        first_name=fio.split()[0] if fio else '',
        last_name=' '.join(fio.split()[1:]) if len(fio.split()) > 1 else ''
    )
    print(f"Пользователь {login} создан")

# 2. Добавляем в группу "Операторы" (тех. персонал)
group, created = Group.objects.get_or_create(name='Операторы')
user.groups.add(group)
if created:
    print("Группа 'Операторы' создана")
print(f"Пользователь добавлен в группу 'Операторы'")

# 3. Создаём запись в таблице core_staff
if hasattr(user, 'staff_profile'):
    print("Запись в core_staff уже существует")
else:
    Staff.objects.create(
        user=user,
        fio=fio,
        role='Оператор',
        start_work=timezone.now(),
        end_work=None  # Пока работает
    )
    print("Запись в core_staff создана")

print("Готово! Теперь можно войти под логином:", login, "паролем:", password)
print("После входа пользователь попадёт на страницу tech.html")
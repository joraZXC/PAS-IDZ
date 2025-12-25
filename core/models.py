from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    phone = models.CharField(max_length=11, blank=True, verbose_name="Телефон")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.user.username

class Quality(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='quality_profile')
    fio = models.CharField(max_length=50, verbose_name="ФИО")

    class Meta:
        verbose_name = "Служба качества"
        verbose_name_plural = "Служба качества"

    def __str__(self):
        return self.fio

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    fio = models.CharField(max_length=50, verbose_name="ФИО")
    role = models.CharField(max_length=100, verbose_name="Роль")

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"

    def __str__(self):
        return self.fio

class Planinggroup(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='planinggroup_profile')
    fio = models.CharField(max_length=50, verbose_name="ФИО")
    role = models.CharField(max_length=37, verbose_name="Роль")
    start_work = models.DateTimeField(null=True, blank=True, verbose_name="Начало работы")
    end_work = models.DateTimeField(null=True, blank=True, verbose_name="Окончание работы")

    class Meta:
        verbose_name = "Группа планирования"
        verbose_name_plural = "Группы планирования"

    def __str__(self):
        return self.fio

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    fio = models.CharField(max_length=50, verbose_name="ФИО")
    role = models.CharField(max_length=37, verbose_name="Роль")
    start_work = models.DateTimeField(
        verbose_name="Начало работы",
        null=True,
        blank=True
    )
    end_work = models.DateTimeField(
        verbose_name="Окончание работы",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Персонал"
        verbose_name_plural = "Персонал"

    def __str__(self):
        return self.fio

class Warehouse(models.Model):
    status = models.CharField(max_length=100, verbose_name="Статус склада")
    total_place = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Общая площадь (м²)")
    free_place = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Свободная площадь (м²)")

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

    def __str__(self):
        return f"Склад — Свободно: {self.free_place} м²"

class Report(models.Model):
    internal_id = models.CharField(max_length=14, unique=True, verbose_name="Внутренний ID")
    date = models.DateTimeField(verbose_name="Дата рапорта")
    info = models.TextField(verbose_name="Содержание рапорта")

    class Meta:
        verbose_name = "Рапорт"
        verbose_name_plural = "Рапорты"
        ordering = ['-date']

    def __str__(self):
        return f"Рапорт {self.internal_id} от {self.date.date()}"

class Order(models.Model):
    internal_id = models.CharField(max_length=15, unique=True, verbose_name="Внутренний номер заказа")
    manager = models.ForeignKey(Manager, on_delete=models.RESTRICT, verbose_name="Менеджер")
    client = models.ForeignKey(Client, on_delete=models.RESTRICT, verbose_name="Клиент")
    date_created = models.DateTimeField(verbose_name="Дата создания")
    date_planned = models.DateTimeField(verbose_name="Планируемая дата")
    date_completed = models.DateTimeField(null=True, blank=True, verbose_name="Дата выполнения")
    status = models.CharField(max_length=15, verbose_name="Статус")
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Стоимость")

    is_ready = models.BooleanField(default=False, verbose_name="Готов к отгрузке")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-date_created']

    def __str__(self):
        return f"Заказ {self.internal_id}"

class Test(models.Model):
    internal_id = models.CharField(max_length=19, unique=True, verbose_name="Внутренний ID теста")
    quality = models.ForeignKey(Quality, on_delete=models.RESTRICT, verbose_name="ОТК")
    start_time = models.DateTimeField(null=True, blank=True, verbose_name="Начало теста")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Окончание теста")
    is_passed = models.BooleanField(null=True, verbose_name="Прошёл?")
    standard_compliant = models.BooleanField(null=True, verbose_name="Соответствует стандарту?")
    info = models.TextField(null=True, blank=True, verbose_name="Результаты/комментарий")

    class Meta:
        verbose_name = "Химический тест"
        verbose_name_plural = "Химические тесты"

    def __str__(self):
        return f"Тест {self.internal_id}"

class Roll(models.Model):
    internal_id = models.CharField(max_length=16, unique=True, verbose_name="Внутренний ID рулона")
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, verbose_name="Заказ")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.RESTRICT, verbose_name="Склад")
    test = models.ForeignKey(Test, on_delete=models.RESTRICT, verbose_name="Тест")
    staff = models.ForeignKey(Staff, on_delete=models.RESTRICT, null=True, blank=True, verbose_name="Ответственный")
    defect = models.ForeignKey('Defect', on_delete=models.RESTRICT, null=True, blank=True, verbose_name="Брак")

    weight = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Вес (т)")
    thickness = models.DecimalField(max_digits=8, decimal_places=4, verbose_name="Толщина (мм)")
    width = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Ширина (мм)")
    status = models.CharField(max_length=100, verbose_name="Статус")
    is_ready = models.BooleanField(default=False, verbose_name="Готов")

    class Meta:
        verbose_name = "Рулон"
        verbose_name_plural = "Рулоны"
        indexes = [
            models.Index(fields=['internal_id']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Рулон {self.internal_id} ({self.weight} т)"

class Defect(models.Model):
    defect_type = models.CharField(max_length=50, verbose_name="Тип брака")
    found_date = models.DateTimeField(verbose_name="Дата обнаружения")
    fixed_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата исправления")
    is_fixed = models.BooleanField(default=False, verbose_name="Исправлен")
    info = models.TextField(verbose_name="Описание")
    staff = models.ForeignKey(Staff, on_delete=models.RESTRICT, null=True, blank=True, verbose_name="Обнаружил")

    class Meta:
        verbose_name = "Брак"
        verbose_name_plural = "Брак"

    def __str__(self):
        return f"Брак: {self.defect_type} ({self.found_date.date()})"

class Downtime(models.Model):
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, null=True, blank=True, verbose_name="Заказ")
    staff = models.ForeignKey(Staff, on_delete=models.RESTRICT, null=True, blank=True, verbose_name="Ответственный")
    start_time = models.DateTimeField(verbose_name="Начало простоя")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Окончание простоя")
    reason = models.CharField(max_length=100, verbose_name="Причина")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    is_fixed = models.BooleanField(default=False, verbose_name="Устранён")

    class Meta:
        verbose_name = "Простой"
        verbose_name_plural = "Простои"

    def __str__(self):
        return f"Простой {self.reason} ({self.start_time.date()})"

class Passport(models.Model):
    internal_id = models.CharField(max_length=15, unique=True, verbose_name="Номер паспорта")
    client = models.ForeignKey(Client, on_delete=models.RESTRICT, verbose_name="Клиент")
    quality = models.ForeignKey(Quality, on_delete=models.RESTRICT, verbose_name="ОТК")
    test = models.ForeignKey(Test, on_delete=models.RESTRICT, null=True, blank=True, verbose_name="Тест")
    info = models.TextField(verbose_name="Содержание")
    created_date = models.DateTimeField(verbose_name="Дата создания")
    issued_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата выдачи")
    is_issued = models.BooleanField(default=False, verbose_name="Выдан")
    is_created = models.BooleanField(default=False, verbose_name="Сформирован")

    class Meta:
        verbose_name = "Паспорт плавки"
        verbose_name_plural = "Паспорта плавки"

    def __str__(self):
        return f"Паспорт {self.internal_id}"

class Route(models.Model):
    planinggroup = models.ForeignKey(Planinggroup, on_delete=models.RESTRICT, verbose_name="Группа планирования")
    staff = models.ForeignKey(Staff, on_delete=models.RESTRICT, verbose_name="Исполнитель")
    approved_date = models.DateTimeField(verbose_name="Дата утверждения")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    current_step = models.PositiveIntegerField(verbose_name="Текущий шаг")
    is_completed = models.BooleanField(default=False, verbose_name="Завершён")

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"

    def __str__(self):
        return f"Маршрут (шаг {self.current_step})"
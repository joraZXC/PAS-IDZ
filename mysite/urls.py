from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

# Импортируем только нужные views
from core.views import (
    CustomLoginView,
    LeadershipView,
    QualityView,
    TechView,
    PlanView,
    ClientView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Главная страница — форма логина
    path('', TemplateView.as_view(template_name='login.html'), name='home'),

    # Вход — используем КАСТОМНЫЙ LoginView с редиректом по роли
    path('login/', CustomLoginView.as_view(), name='login'),

    # Выход
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # Ролевые страницы
    path('rukvo/', LeadershipView.as_view(), name='rukvo'),
    path('quality/', QualityView.as_view(), name='quality'),
    path('tech/', TechView.as_view(), name='tech'),
    path('plan/', PlanView.as_view(), name='plan'),
    path('client/', ClientView.as_view(), name='client'),
]
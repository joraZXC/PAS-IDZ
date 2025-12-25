from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from .models import Order, Roll, Passport, Report, Downtime, Defect, Warehouse, Route, Test


# Базовый миксин для проверки роли
class RoleRequiredMixin(UserPassesTestMixin):
    allowed_groups = []

    def test_func(self):
        return self.request.user.groups.filter(name__in=self.allowed_groups).exists()


# КАСТОМНЫЙ LOGIN VIEW — ЭТО ГЛАВНОЕ ИСПРАВЛЕНИЕ
class CustomLoginView(DjangoLoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user

        if user.groups.filter(name='Руководство').exists():
            return reverse_lazy('rukvo')
        if user.groups.filter(name='ОТК').exists():
            return reverse_lazy('quality')
        if user.groups.filter(name='Операторы').exists():
            return reverse_lazy('tech')
        if user.groups.filter(name='Планирование').exists():
            return reverse_lazy('plan')
        if user.groups.filter(name='Заказчики').exists():
            return reverse_lazy('client')

        # Если ни одна группа не подходит — возвращаем на главную
        return reverse_lazy('home')


# Страница руководства
class LeadershipView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = 'rukvo.html'
    allowed_groups = ['Руководство']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        context['reports'] = Report.objects.all()
        context['current_date'] = '17.12.2025'
        return context


# Страница ОТК
class QualityView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = 'quality.html'
    allowed_groups = ['ОТК']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tests'] = Test.objects.all()
        context['passports'] = Passport.objects.all()
        context['rolls'] = Roll.objects.filter(defect__isnull=False)
        return context


# Страница оператора (технический персонал)
class TechView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = 'tech.html'
    allowed_groups = ['Операторы']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rolls'] = Roll.objects.all()
        context['downtimes'] = Downtime.objects.all()
        context['defects'] = Defect.objects.all()
        context['reports'] = Report.objects.all()
        return context


# Страница планирования
class PlanView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = 'plan.html'
    allowed_groups = ['Планирование']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        context['warehouses'] = Warehouse.objects.all()
        context['routes'] = Route.objects.all()
        return context


# Страница заказчика
class ClientView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = 'client.html'
    allowed_groups = ['Заказчики']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(client__user=self.request.user)
        context['passports'] = Passport.objects.filter(client__user=self.request.user)
        return context
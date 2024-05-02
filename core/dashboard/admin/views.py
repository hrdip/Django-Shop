from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from accounts.models import UserType
# Create your views here.


class AdminDashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/admin/home.html'


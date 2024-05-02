from django.views.generic import  TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.auth import views as auth_views
from dashboard.admin.forms import AdminPasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.


class AdminDashboardHomeView(LoginRequiredMixin,HasAdminAccessPermission, TemplateView):
    template_name = 'dashboard/admin/home.html'

class AdminSecurityEditView(LoginRequiredMixin,HasAdminAccessPermission, TemplateView, SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name  = 'dashboard/admin/profile/security-edit.html'
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy("dashboard:admin:admin-security-edit")
    success_message = "Your password was successfully changed"
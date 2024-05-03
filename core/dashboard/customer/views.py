from django.views.generic import  TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasCustomerAccessPermission
from django.contrib.auth import views as auth_views
from dashboard.customer.forms import CustomerPasswordChangeForm, CustomerProfileEditForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import Profile

# Create your views here.


class CustomerDashboardHomeView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = 'dashboard/customer/home.html'

class CustomerSecurityEditView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView, SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name  = 'dashboard/customer/profile/security-edit.html'
    form_class = CustomerPasswordChangeForm
    success_url = reverse_lazy("dashboard:customer:customer-security-edit")
    success_message = "Your password was successfully changed"


class CustomerProfileEditView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, UpdateView):
    template_name  = 'dashboard/customer/profile/profile-edit.html'
    form_class = CustomerProfileEditForm
    success_url = reverse_lazy("dashboard:customer:customer-profile-edit")
    success_message = "Your profile was successfully updated."

    # get the data of this user (becuse we want updated profile)
    def get_object(self,queryset=None):
        return Profile.objects.get(user=self.request.user)
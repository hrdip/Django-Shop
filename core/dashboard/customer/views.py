from django.views.generic import  TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasCustomerAccessPermission
from django.contrib.auth import views as auth_views
from dashboard.customer.forms import CustomerPasswordChangeForm, CustomerProfileEditForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import Profile
from django.shortcuts import redirect
from django.contrib import messages
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
    

class CustomerProfileImageEditView(LoginRequiredMixin,HasCustomerAccessPermission, SuccessMessageMixin, UpdateView):
    
    # in UpdateView we need template_name but for here we dont want use, then we need to explain to UpdateView we dont need to use yor 'get' and only want use your 'post'
    http_method_names = ['post']
    model = Profile
    fields = ['image']
    success_url = reverse_lazy("dashboard:customer:customer-profile-edit")
    success_message = "Your profile image was successfully updated."
    
    # get the data of this user (becuse we want updated profile)
    def get_object(self,queryset=None):
        return Profile.objects.get(user=self.request.user)
    
    # if faild to update
    # if form is not valid need to redirect to template_name and we are not set. then we need to explain redirect to success url
    def form_invalid(self, form):
        messages.error(self.request,"updated image has failed please try again")
        return redirect (self.success_url)
from django.views.generic import  TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.auth import views as auth_views
from dashboard.admin.forms import AdminPasswordChangeForm, AdminProfileEditForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import Profile
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.

class AdminSecurityEditView(LoginRequiredMixin, HasAdminAccessPermission, TemplateView, SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name  = 'dashboard/admin/profile/security-edit.html'
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy("dashboard:admin:admin-security-edit")
    success_message = "Your password was successfully changed"


class AdminProfileEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    template_name  = 'dashboard/admin/profile/profile-edit.html'
    form_class = AdminProfileEditForm
    success_url = reverse_lazy("dashboard:admin:admin-profile-edit")
    success_message = "Your profile was successfully updated."

    # get the data of this user (because we want updated profile)
    def get_object(self,queryset=None):
        return Profile.objects.get(user=self.request.user)


class AdminProfileImageEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    
    # in UpdateView we need template_name but for here we dont want use, then we need to explain to UpdateView we dont need to use yor 'get' and only want use your 'post'
    http_method_names = ['post']
    model = Profile
    fields = ['image']
    success_url = reverse_lazy("dashboard:admin:admin-profile-edit")
    success_message = "Your profile image was successfully updated."
    
    # get the data of this user (because we want updated profile)
    def get_object(self,queryset=None):
        return Profile.objects.get(user=self.request.user)
    
    # if failed to update
    # if form is not valid need to redirect to template_name and we are not set. then we need to explain redirect to success url
    def form_invalid(self, form):
        messages.error(self.request,"updated image has failed please try again")
        return redirect (self.success_url)
    
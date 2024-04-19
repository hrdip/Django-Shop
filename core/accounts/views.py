from django.shortcuts import render
from django.contrib.auth import views as auth_views
from . forms import AuthenticationForm
from django.core.mail import send_mail
# Create your views here.

class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True

class CustomLogoutView(auth_views.LogoutView):
    pass

class CustomPasswordResetView(auth_views.PasswordResetView):
    email_template_name = "accounts/password_reset_email.txt"
    success_url = '/accounts/password_reset/done/'
    template_name = "accounts/password_reset_form.html"


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = '/accounts/reset/done/'

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"


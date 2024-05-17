from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . forms import AuthenticationForm
# register user 
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from .forms import UserCreateForm


class RegisterUserView(FormView):
    template_name = 'accounts/register_user.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
               
        # Use the custom user model in authenticate
        user = authenticate( email=email, password=password)
        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RegisterUserView, self).get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context




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


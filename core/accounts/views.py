from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . forms import AuthenticationForm, UserCreateForm, ProfileCreateForm
# register user 
from django.contrib.auth import login
from django.views.generic.edit import FormView
# activate user
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import login
from django.views import View
from .tokens import account_activation_token
from .models import User, Profile
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
import logging
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


logger = logging.getLogger(__name__)

class RegisterUserView(FormView):
    template_name = 'accounts/register_user.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('accounts:verify-email-send')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account.'
        message = render_to_string('accounts/verify_user_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        try:
            email.send()
            logger.info(f"Activation email sent to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send activation email to {to_email}: {e}")
        
        form.save()
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RegisterUserView, self).get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context


class VerifyUserView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            login(request, user)
            return redirect('accounts:profile-update')
        else:
            return render(request, 'verify_user_invalid.html')
        

class VerifyEmailSend(TemplateView):
    template_name = 'accounts/verify_user_done.html'


class ProfileUserView(TemplateView, LoginRequiredMixin):
    template_name = 'accounts/profile_user.html'

    def get(self, request, *args, **kwargs):
        try:
            profile = request.user.user_profile
        except Profile.DoesNotExist:
            profile = None
        
        if profile:
            form = ProfileCreateForm(instance=profile)
        else:
            form = ProfileCreateForm()

        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        try:
            profile = request.user.user_profile
            form = ProfileCreateForm(request.POST, request.FILES, instance=profile)
        except Profile.DoesNotExist:
            form = ProfileCreateForm(request.POST, request.FILES)
        
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('website:index')
        
        return self.render_to_response({'form': form})



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


from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django import forms
from accounts.models import User



class AuthenticationForm (auth_forms.AuthenticationForm):
    def confirm_login_allowed(self, user):
        # do everiting happend in parent class
        super(AuthenticationForm, self).confirm_login_allowed(user)
        # add this to the parent class for customization
        if not user.is_verified:
            raise ValidationError("user is not verified")


class UserCreateForm(auth_forms.UserCreationForm):
    
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit: 
            user.save()
        return user
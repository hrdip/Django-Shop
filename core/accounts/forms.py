from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError

class AuthenticationForm (auth_forms.AuthenticationForm):
    def confirm_login_allowed(self, user):
        # do everiting happend in parent class
        super(AuthenticationForm, self).confirm_login_allowed(user)
        # add this to the parent class for customization
        if not user.is_verified:
            raise ValidationError("user is not verified")


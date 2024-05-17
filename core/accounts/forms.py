from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django import forms
from accounts.models import User, Profile



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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = "یک ایمیل معتبر وارد نمایید"
        self.fields['password1'].widget.attrs['placeholder'] = "رمز عبور خود را وارد نمایید"
        self.fields['password2'].widget.attrs['placeholder'] = "تکرار رمز عبور"


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = "نام خود را وارد نمایید"
        self.fields['last_name'].widget.attrs['placeholder'] = "نام خانوادگی خود را وارد نمایید"
        self.fields['phone_number'].widget.attrs['placeholder'] = "تلفن تماس خود را وارد نمایید "
        self.fields['image'].widget.attrs['placeholder'] = "عکس پروفایل خود را اپلود کنید"
        self.fields["phone_number"].widget.attrs['type'] = 'number'
        self.fields['image'].widget.attrs['type'] = "image"
from django.forms import ModelForm
from .models import ContactUsModel

class ContactUsForm(ModelForm):
    class Meta:
        model = ContactUsModel
        fields = "__all__"
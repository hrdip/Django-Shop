from django.forms import ModelForm
from .models import ContactUsModel, NewsLetterModel

class ContactUsForm(ModelForm):
    class Meta:
        model = ContactUsModel
        fields = "__all__"

class NewsLetterForm(ModelForm):
    class Meta:
        model = NewsLetterModel
        fields = ("email",)
from django.contrib import admin
from .models import ContactUsModel


# Register your models here.
class CustomContactUsAdmin(admin.ModelAdmin):
    model = ContactUsModel
    list_display = ("first_name", "last_name", "email", "phone_number","subject")
    list_filter = ("first_name", "last_name", "email", "phone_number", "subject")
    searching_fields = ("first_name", "last_name", "subject")


admin.site.register(ContactUsModel, CustomContactUsAdmin)
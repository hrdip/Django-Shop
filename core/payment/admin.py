from django.contrib import admin
from .models import PaymentModel
# Register your models here.

class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ("id", "authority_id", "amount", "response_code", "status", "created_date")



admin.site.register(PaymentModel, PaymentModelAdmin)

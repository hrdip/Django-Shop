from django.contrib import admin
from .models import ReviewModel
# Register your models here.

class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "rate", "status", "created_date")



admin.site.register(ReviewModel, ReviewModelAdmin)
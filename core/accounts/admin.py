from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile
from django.contrib.auth import get_user_model

# for dynamically generated
User = get_user_model( )

class CustomUserAdmin(UserAdmin):
    model = User
    # add_form = CustomUserCreationsForm
    # change_password_form = CustomUserChangePasswordForm
    list_display = ("id", "email", "is_superuser", "is_active", "is_verified")
    list_filter = ("email", "is_superuser", "is_active", "is_verified")
    searching_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "is_verified",
                ),
            },
        ),
        (
            "Group permissions",
            {
                "fields": ("groups", "user_permissions", "type"),
            },
        ),
        (
            "Important date",
            {
                "fields": ("last_login",),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                    "type"
                ),
            },
        ),
    )


class CustomProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user","first_name", "last_name", "phone_number")
    searching_fields = ("user", "first_name", "last_name", "phone_number")



admin.site.register(Profile, CustomProfileAdmin)
admin.site.register(User, CustomUserAdmin)
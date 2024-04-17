from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from . validators import validate_cellphone_number
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

class UserType(models.IntegerChoices):
    customer = 1 , _("customer")
    admin = 2 , _("admin")
    superuser = 3 , _("superuser")


class UserManager(BaseUserManager):
    """custom user model manager where email is the uniqu identifiers
    for authentication instead of username
    """

    def create_user(self, email, password, **extra_fields):
        """
        create and sava a user with the given
        emial and password and extra data
        """
        if not email:
            raise ValueError(_("the email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        create and sava a superuser with the given
        emial and password
        """
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("type", UserType.superuser.value)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    custom User Model for our app
    """

    email = models.EmailField(max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    type = models.IntegerField(choices=UserType.choices, default=UserType.customer.value)

    objects = UserManager()
    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11, validators=[validate_cellphone_number])
    image = models.ImageField(blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def get_fullname(self):
        if self.first_name or self.last_name:
            return self.first_name + " " + self.last_name
        return "کاربر جدید"


# signal properties
# create profile base on Profile class
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and instance.type == UserType.customer.value:
        # pk for equality user id and profile id insted of auto increment
        Profile.objects.create(pk=instance.pk, user=instance)

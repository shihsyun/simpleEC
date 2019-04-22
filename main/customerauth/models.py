from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomerManager, VerifyCodeManager
from django.conf import settings


class Customer(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField('email address', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomerManager()

    def __str__(self):
        return self.name


class VerifyCode(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField('code', max_length=40, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = VerifyCodeManager()

    def __str__(self):
        return self.code

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    class UserChoice(models.TextChoices):
        COMM_PERSONNEL = ("COMM_PERSONNEL", "Community Personnel",)
        ADMIN = ("ADMIN", "Admin",)
        PUBLIC_OFFICER = ("PUBLIC OFFICER", "Public Officer",)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.CharField(max_length=100, choices=UserChoice.choices, default=UserChoice.ADMIN)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_added = models.DateField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ["-date_added"]

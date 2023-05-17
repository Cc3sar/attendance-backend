from django.contrib.auth.models import AbstractUser
from django.db import models

from .CustomUserManager import CustomUserManager


class User(AbstractUser):
    """
        Custom user model
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email\
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.first_name
    
    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
        return True
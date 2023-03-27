from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class AdminUser(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        ]

    def __str__(self):
        return self.last_name

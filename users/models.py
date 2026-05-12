from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member'
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username